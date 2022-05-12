# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from asyncio import Task, create_task, shield, wait_for
from typing import Any, Dict, Optional

from overrides import overrides


async def _timeout_wrapper(coro, timeout: Optional[float] = None) -> Any:
    if timeout is not None:
        assert timeout > 0
        return await wait_for(coro, timeout=timeout)
    else:
        return await coro


class TaskManagerInterface(metaclass=ABCMeta):
    @abstractmethod
    def on_done(self, task: Task) -> None:
        raise NotImplementedError


class TaskManager(TaskManagerInterface, Dict[str, Task]):
    async def close(self) -> None:
        for task in self.values():
            task.cancel()
            try:
                await task
            except:  # noqa
                pass
        self.clear()

    async def join(self, key: str, timeout: Optional[float] = None) -> Any:
        task = self.__getitem__(key)
        if timeout is not None:
            assert timeout > 0
            return await wait_for(shield(task), timeout=timeout)
        else:
            return await task

    def create_task(self, key: str, coro, timeout: Optional[float] = None) -> Task:
        if self.__contains__(key):
            raise KeyError(f"Already exists key: {key}")
        task = create_task(_timeout_wrapper(coro, timeout), name=key)
        task.add_done_callback(self.on_done)
        self.__setitem__(key, task)
        return task

    @overrides
    def on_done(self, task: Task) -> None:
        assert isinstance(task, Task)


class AutoRemoveTaskManager(TaskManager):
    @overrides
    def on_done(self, task: Task) -> None:
        assert isinstance(task, Task)
        self.__delitem__(task.get_name())
