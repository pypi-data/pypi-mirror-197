from typing import Dict

from scaled.protocol.python.message import Task, TaskResult
from scaled.scheduler.mixins import ClientManager, Looper


class VanillaClientManager(ClientManager, Looper):
    def __init__(self):
        pass

    async def on_task_new(self, client: bytes, task: Task):
        pass

    async def on_task_cancel(self, client: bytes, task_id: bytes):
        pass

    async def on_task_done(self, result: TaskResult):
        pass

    async def loop(self):
        pass

    async def statistics(self) -> Dict:
        pass
