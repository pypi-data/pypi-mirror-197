import asyncio
import json
import logging

from scaled.io.config import CLEANUP_INTERVAL_SECONDS
from scaled.scheduler.client_manager.vanilla import VanillaClientManager
from scaled.scheduler.function_manager.vanilla import VanillaFunctionManager
from scaled.utility.event_loop import create_async_loop_routine
from scaled.utility.zmq_config import ZMQConfig
from scaled.io.async_binder import AsyncBinder
from scaled.protocol.python.message import MessageType, MessageVariant, MonitorRequest, MonitorResponse
from scaled.scheduler.task_manager.vanilla import VanillaTaskManager
from scaled.scheduler.worker_manager.vanilla import VanillaWorkerManager


class Scheduler:
    def __init__(
        self,
        address: ZMQConfig,
        io_threads: int,
        max_number_of_tasks_waiting: int,
        per_worker_queue_size: int,
        worker_timeout_seconds: int,
        function_retention_seconds: int,
        load_balance_seconds: int,
        load_balance_trigger_times: int,
    ):
        self._address = address

        self._binder = AsyncBinder(prefix="S", address=self._address, io_threads=io_threads)
        self._client_manager = VanillaClientManager()
        self._function_manager = VanillaFunctionManager(function_retention_seconds=function_retention_seconds)
        self._task_manager = VanillaTaskManager(max_number_of_tasks_waiting=max_number_of_tasks_waiting)
        self._worker_manager = VanillaWorkerManager(
            per_worker_queue_size=per_worker_queue_size,
            timeout_seconds=worker_timeout_seconds,
            load_balance_seconds=load_balance_seconds,
            load_balance_trigger_times=load_balance_trigger_times,
        )

        self._binder.register(self.on_receive_message)
        self._function_manager.hook(self._binder)
        self._task_manager.hook(self._binder, self._function_manager, self._worker_manager)
        self._worker_manager.hook(self._binder, self._task_manager)

    async def on_receive_message(self, source: bytes, message_type: MessageType, message: MessageVariant):
        if message_type == MessageType.Heartbeat:
            await self._worker_manager.on_heartbeat(source, message)
            return

        if message_type == MessageType.BalanceResponse:
            await self._worker_manager.on_balance_response(message)
            return

        if message_type == MessageType.MonitorRequest:
            await self.statistics(source, message)
            return

        if message_type == MessageType.Task:
            await self._task_manager.on_task_new(source, message)
            return

        if message_type == MessageType.TaskCancel:
            await self._task_manager.on_task_cancel(source, message)
            return

        if message_type == MessageType.TaskCancelEcho:
            await self._worker_manager.on_task_cancel_echo(source, message)
            return

        if message_type == MessageType.TaskResult:
            await self._worker_manager.on_task_done(message)
            return

        if message_type == MessageType.FunctionRequest:
            await self._function_manager.on_function(source, message)
            return

        logging.error(f"{self.__class__.__name__}: unknown {message_type} from {source=}: {message}")

    async def get_loops(self):
        try:
            await asyncio.gather(
                create_async_loop_routine(self._binder.routine, 0),
                create_async_loop_routine(self._task_manager.routine, 0),
                create_async_loop_routine(self._function_manager.routine, CLEANUP_INTERVAL_SECONDS),
                create_async_loop_routine(self._worker_manager.routine, CLEANUP_INTERVAL_SECONDS),
                return_exceptions=True,
            )
        except asyncio.CancelledError:
            pass

    async def statistics(self, source: bytes, request: MonitorRequest):
        assert isinstance(request, MonitorRequest)
        stats = MonitorResponse(
            json.dumps(
                {
                    "binder": await self._binder.statistics(),
                    "task_manager": await self._task_manager.statistics(),
                    "worker_manager": await self._worker_manager.statistics(),
                    "function_manager": await self._function_manager.statistics(),
                }
            ).encode()
        )
        await self._binder.send(source, MessageType.MonitorResponse, stats)
