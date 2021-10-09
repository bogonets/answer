# -*- coding: utf-8 -*-

from typing import Dict, Union, Callable, Awaitable
from inspect import iscoroutinefunction

Watcher = Callable[..., Union[Awaitable[None], None]]


class WatcherContainer(Dict[str, Watcher]):
    def call_synced_watcher(self, name: str, *args, **kwargs) -> None:
        watcher = self.__getitem__(name)
        if iscoroutinefunction(watcher):
            raise RuntimeError("It's not an awaitable watcher")
        else:
            watcher(*args, **kwargs)

    async def call_watcher(self, name: str, *args, **kwargs) -> None:
        watcher = self.__getitem__(name)
        if iscoroutinefunction(watcher):
            await watcher(*args, **kwargs)  # type: ignore[misc]
        else:
            watcher(*args, **kwargs)
