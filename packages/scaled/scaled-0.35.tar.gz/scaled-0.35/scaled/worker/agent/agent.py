import zmq.asyncio

from scaled.io.async_connector import AsyncConnector
from scaled.protocol.python.message import MessageType, MessageVariant
from scaled.utility.zmq_config import ZMQConfig
from scaled.worker.agent.function_cache import FunctionCache
from scaled.worker.agent.heart_beat import WorkerHeartbeat
from scaled.worker.agent.worker_task_manager import WorkerTaskManager


class Agent:
    def __init__(
        self,
        external_address: ZMQConfig,
        internal_context: zmq.asyncio.Context,
        internal_address: ZMQConfig,
        heartbeat_interval_seconds: int,
        function_retention_seconds: int,
        per_worker_processing_queue_size: int,
    ):
        self._connector_external = AsyncConnector(
            prefix="W",
            context=zmq.asyncio.Context(),
            socket_type=zmq.DEALER,
            address=external_address,
            bind_or_connect="connect",
            callback=self.on_receive_external,
        )

        self._connector_internal = AsyncConnector(
            prefix="AA",
            context=internal_context,
            socket_type=zmq.PAIR,
            address=internal_address,
            bind_or_connect="bind",
            callback=self.on_receive_internal,
            send_high_watermark=per_worker_processing_queue_size,
        )

        self._task_manager = WorkerTaskManager(connector_internal=self._connector_internal)

        self._function_cache = FunctionCache(
            connector_external=self._connector_external,
            task_manager=self._task_manager,
            function_retention_seconds=function_retention_seconds,
        )

        self._heartbeat = WorkerHeartbeat(
            connector_external=self._connector_external,
            task_manager=self._task_manager,
            heartbeat_interval_seconds=heartbeat_interval_seconds,
        )

    @property
    def identity(self):
        return self._connector_external.identity

    async def on_receive_external(self, message_type: MessageType, message: MessageVariant):
        if message_type == MessageType.Task:
            await self._function_cache.on_new_task(message)
            return

        if message_type == MessageType.BalanceRequest:
            await self._function_cache.on_balance_request(message)
            return

        if message_type == MessageType.FunctionResponse:
            await self._function_cache.on_new_function(message)
            return

        raise TypeError(f"Unknown {message_type=} {message=}")

    async def on_receive_internal(self, message_type: MessageType, message: MessageVariant):
        if message_type == MessageType.TaskResult:
            await self._function_cache.on_task_result(message)
            return

        raise TypeError(f"Unknown {message_type=} {message=}")

    def get_loops(self):
        return [
            self._connector_external.loop,
            self._connector_internal.loop,
            self._task_manager.loop,
            self._heartbeat.loop,
            self._function_cache.loop,
        ]
