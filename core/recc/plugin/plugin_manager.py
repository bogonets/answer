# -*- coding: utf-8 -*-

from typing import Dict, Any
from pathlib import Path
from asyncio import gather
from recc.plugin.plugin import Plugin

PLUGIN_SCRIPT_EXTENSION = ".py"


class PluginManager(Dict[str, Plugin]):
    def create(self, context: Any, *dirs: Path) -> None:
        for directory in dirs:
            assert directory.is_dir()

            name = directory.name
            script_path = directory / (name + PLUGIN_SCRIPT_EXTENSION)

            if not script_path.is_file():
                raise FileNotFoundError(f"Plugin script not found: {script_path}")

            plugin = Plugin(str(script_path))
            if plugin.exists_create:
                plugin.call_create(context)
            self.__setitem__(plugin.name, plugin)

    def destroy(self) -> None:
        for key, plugin in self.items():
            if plugin.exists_destroy:
                plugin.call_destroy()

    async def open(self) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_open:
                coroutines.append(plugin.call_open())
        await gather(*coroutines)

    async def close(self) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_close:
                coroutines.append(plugin.call_close())
        await gather(*coroutines)
