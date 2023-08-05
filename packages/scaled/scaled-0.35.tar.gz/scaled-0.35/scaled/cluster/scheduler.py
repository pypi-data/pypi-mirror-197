import asyncio
import multiprocessing
from typing import Literal, Optional

from scaled.utility.event_loop import register_event_loop
from scaled.utility.zmq_config import ZMQConfig
from scaled.scheduler.main import Scheduler
from scaled.utility.logging.utility import setup_logger


class SchedulerProcess(multiprocessing.get_context("spawn").Process):
    def __init__(
        self,
        address: ZMQConfig,
        io_threads: int,
        max_number_of_tasks_waiting: int,
        per_worker_queue_size: int,
        worker_timeout_seconds: int,
        function_retention_seconds: int,
        event_loop: Literal["builtin", "uvloop"] = "builtin",
    ):
        multiprocessing.Process.__init__(self, name="Scheduler")
        self._address = address
        self._io_threads = io_threads
        self._max_number_of_tasks_waiting = max_number_of_tasks_waiting
        self._per_worker_queue_size = per_worker_queue_size
        self._worker_timeout_seconds = worker_timeout_seconds
        self._function_retention_seconds = function_retention_seconds
        self._event_loop = event_loop
        self._scheduler: Optional[Scheduler] = None
        self._loop = None

    def run(self) -> None:
        # scheduler have its own single process
        setup_logger()
        self._scheduler = Scheduler(
            address=self._address,
            io_threads=self._io_threads,
            max_number_of_tasks_waiting=self._max_number_of_tasks_waiting,
            per_worker_queue_size=self._per_worker_queue_size,
            worker_timeout_seconds=self._worker_timeout_seconds,
            function_retention_seconds=self._function_retention_seconds,
        )

        register_event_loop(self._event_loop)

        self._loop = asyncio.get_event_loop()
        for coroutine in self._scheduler.get_loops():
            self._loop.create_task(coroutine())
        self._loop.run_forever()
