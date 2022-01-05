# -*- coding: utf-8 -*-

from typing import Dict, Any
from asyncio import Task, CancelledError, ensure_future
from asyncio import sleep as asyncio_sleep


class Sleeper:
    def __init__(self):
        self.tasks: Dict[Any, Task] = dict()

    async def sleep(self, key: Any, seconds: float, result=None, *, loop=None) -> Any:
        coro = asyncio_sleep(seconds, result=result, loop=loop)
        task = ensure_future(coro)
        self.tasks[key] = task
        try:
            return await task
        except CancelledError:
            return result
        finally:
            del self.tasks[key]

    def cancel(self, key: Any) -> None:
        self.tasks[key].cancel()

    def cancel_all(self) -> None:
        for task in self.tasks.values():
            task.cancel()
