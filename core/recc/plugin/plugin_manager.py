# -*- coding: utf-8 -*-

from asyncio import gather
from pathlib import Path
from typing import Any, Dict

from recc.plugin.plugin import Plugin

PLUGIN_SCRIPT_EXTENSION = ".py"


class PluginManager(Dict[str, Plugin]):
    def call_create(self, context: Any, *dirs: Path) -> None:
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

    def call_destroy(self) -> None:
        for key, plugin in self.items():
            if plugin.exists_destroy:
                plugin.call_destroy()

    async def call_create_group(self, group: str) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_create_group:
                coroutines.append(plugin.call_create_group(group))
        await gather(*coroutines)

    async def call_delete_group(self, group: str) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_delete_group:
                coroutines.append(plugin.call_delete_group(group))
        await gather(*coroutines)

    async def call_create_project(self, group: str, project: str) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_create_project:
                coroutines.append(plugin.call_create_project(group, project))
        await gather(*coroutines)

    async def call_delete_project(self, group: str, project: str) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_delete_project:
                coroutines.append(plugin.call_delete_project(group, project))
        await gather(*coroutines)

    async def call_open(self) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_open:
                coroutines.append(plugin.call_open())
        await gather(*coroutines)

    async def call_close(self) -> None:
        coroutines = []
        for key, plugin in self.items():
            if plugin.exists_close:
                coroutines.append(plugin.call_close())
        await gather(*coroutines)
