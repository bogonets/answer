# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction
from typing import Any, Awaitable, Callable, Dict, Union

Watcher = Callable[..., Union[Awaitable[Any], Any]]


class WatcherContainer(Dict[str, Watcher]):
    def call_synced_watcher(self, name: str, *args, **kwargs) -> Any:
        watcher = self.__getitem__(name)
        if iscoroutinefunction(watcher):
            raise RuntimeError("It's not an awaitable watcher")
        return watcher(*args, **kwargs)

    async def call_watcher(self, name: str, *args, **kwargs) -> Any:
        watcher = self.__getitem__(name)
        if iscoroutinefunction(watcher):
            return await watcher(*args, **kwargs)  # type: ignore[misc]
        else:
            return watcher(*args, **kwargs)
