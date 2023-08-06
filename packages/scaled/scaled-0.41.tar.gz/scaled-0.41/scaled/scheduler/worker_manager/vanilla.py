import logging
import time
from typing import Dict, List, Optional, Tuple

from scaled.io.async_binder import AsyncBinder
from scaled.scheduler.mixins import Looper, TaskManager, WorkerManager
from scaled.protocol.python.message import (
    BalanceRequest,
    BalanceResponse,
    Heartbeat,
    MessageType,
    Task,
    TaskCancelEcho,
    TaskEchoStatus,
    TaskResult,
    TaskCancel,
)
from scaled.scheduler.worker_manager.allocators.queued import QueuedAllocator

POLLING_TIME = 1


class VanillaWorkerManager(WorkerManager, Looper):
    def __init__(
        self,
        per_worker_queue_size: int,
        timeout_seconds: int,
        load_balance_seconds: int,
        load_balance_trigger_times: int,
    ):
        self._timeout_seconds = timeout_seconds
        self._load_balance_seconds = load_balance_seconds
        self._load_balance_trigger_times = load_balance_trigger_times

        self._binder: Optional[AsyncBinder] = None
        self._task_manager: Optional[TaskManager] = None

        self._worker_alive_since: Dict[bytes, Tuple[float, Heartbeat]] = dict()
        self._allocator = QueuedAllocator(per_worker_queue_size)

        self._last_balance_advice = None
        self._load_balance_advice_same_count = 0

    def hook(self, binder: AsyncBinder, task_manager: TaskManager):
        self._binder = binder
        self._task_manager = task_manager

    async def on_heartbeat(self, worker: bytes, info: Heartbeat):
        if self._allocator.add_worker(worker):
            logging.info(f"worker {worker} connected")

        self._worker_alive_since[worker] = (time.time(), info)

    async def assign_task_to_worker(self, task: Task) -> bool:
        worker = self._allocator.assign_task(task.task_id)
        if worker is None:
            return False

        # send to worker
        await self._binder.send(worker, MessageType.Task, task)
        return True

    async def on_task_cancel(self, client: bytes, task_cancel: TaskCancel):
        worker = self._allocator.get_assigned_worker(task_cancel.task_id)
        if worker is None:
            logging.error(f"cannot find task_id={task_cancel.task_id.hex()} in task workers")
            return

        await self._binder.send(worker, MessageType.TaskCancel, TaskCancel(task_cancel.task_id))

    async def on_task_cancel_echo(self, worker: bytes, task_cancel_echo: TaskCancelEcho):
        if task_cancel_echo.status == TaskEchoStatus.CancelFailed:
            logging.warning(f"cancel task task_id={task_cancel_echo.task_id.hex()} failed")
            return

        assert task_cancel_echo.status == TaskEchoStatus.CancelOK
        worker = self._allocator.remove_task(task_cancel_echo.task_id)
        if worker is None:
            logging.error(
                f"received TaskCancelEcho for task_id={task_cancel_echo.task_id.hex()} not known to any worker"
            )
            return

        await self._task_manager.on_task_cancel_echo(worker, task_cancel_echo)

    async def on_task_done(self, task_result: TaskResult):
        worker = self._allocator.remove_task(task_result.task_id)
        if worker is None:
            logging.error(
                f"received task_id={task_result.task_id.hex()} not known to any worker, might due to worker get "
                f"disconnected or canceled"
            )
            return

        await self._task_manager.on_task_done(task_result)

    async def on_balance_response(self, response: BalanceResponse):
        task_ids = []
        for task_id in response.task_ids:
            worker = self._allocator.remove_task(task_id)
            if worker is None:
                continue

            task_ids.append(task_id)

        await self.__reroute_tasks(task_ids=task_ids)

    async def has_available_worker(self) -> bool:
        return self._allocator.has_available_worker()

    async def routine(self):
        await self.__balance_request()
        await self.__clean_workers()

    async def statistics(self) -> Dict:
        worker_to_task_numbers = self._allocator.statistics()
        return {
            "scheduler_total_free": sum(worker["scheduler_free"] for worker in worker_to_task_numbers.values()),
            "scheduler_total_running": sum(worker["scheduler_running"] for worker in worker_to_task_numbers.values()),
            "worker_total_queued_tasks": sum(info.queued_tasks for _, (_, info) in self._worker_alive_since.items()),
            "workers": {
                worker.decode(): {
                    "worker_cpu": round(info.cpu_usage, 2),
                    "worker_rss": info.rss_size,
                    "worker_queued_tasks": info.queued_tasks,
                    **worker_to_task_numbers[worker],
                }
                for worker, (last, info) in self._worker_alive_since.items()
            },
        }

    async def __balance_request(self):
        if self._load_balance_seconds <= 0:
            return

        current_advice = self._allocator.balance()
        if self._last_balance_advice != current_advice:
            self._last_balance_advice = current_advice
            self._load_balance_advice_same_count = 1
            return

        self._load_balance_advice_same_count += 1
        if self._load_balance_advice_same_count != self._load_balance_trigger_times:
            return

        if not current_advice:
            return

        logging.info(f"balance: {current_advice}")
        self._last_balance_advice = current_advice
        for worker, number_of_tasks in current_advice.items():
            await self._binder.send(worker, MessageType.BalanceRequest, BalanceRequest(number_of_tasks))

    async def __clean_workers(self):
        now = time.time()
        dead_workers = [
            dead_worker
            for dead_worker, (alive_since, info) in self._worker_alive_since.items()
            if now - alive_since > self._timeout_seconds
        ]
        for dead_worker in dead_workers:
            logging.info(f"worker {dead_worker} disconnected")
            self._worker_alive_since.pop(dead_worker)

            task_ids = self._allocator.remove_worker(dead_worker)
            if not task_ids:
                continue

            logging.info(f"rerouting {len(task_ids)} tasks")
            await self.__reroute_tasks(task_ids)

    async def __reroute_tasks(self, task_ids: List[bytes]):
        for task_id in task_ids:
            await self._task_manager.on_task_reroute(task_id)
