# -*- coding: utf-8 -*-

from asyncio import gather
from re import Pattern
from typing import Dict, List, Optional, Sequence, Union

from recc.logging.logging import recc_plugin_logger as logger
from recc.package.package_utils import filter_module_names
from recc.packet.plugin import PluginA
from recc.plugin.core_plugin import CorePlugin


class CorePluginManager:
    def __init__(
        self,
        prefix: str,
        context=None,  # Do not use type annotation. reason: circular reference.
        denies: Optional[Sequence[Union[str, Pattern]]] = None,
        allows: Optional[Sequence[Union[str, Pattern]]] = None,
    ):
        module_names = filter_module_names(
            prefix=prefix,
            denies=denies,
            allows=allows,
        )
        prefix_length = len(prefix)

        logger.debug(f"Core plugin prefix: '{prefix}'")
        logger.debug(f"Core plugin denies: {denies}")
        logger.debug(f"Core plugin allows: {allows}")
        logger.debug(f"Found the core plugins: {module_names}")

        plugins = dict()

        for module_name in module_names:
            key = module_name[prefix_length:]
            plugin = CorePlugin(module_name)

            logger.info(f"Create Plugin<{key}> version: {plugin.version}")

            if plugin.has_on_create:
                logger.debug(f"Plugin<{key}> Calling on_create ...")
                plugin.on_create(context=context)
                logger.info(f"Plugin<{key}> Called on_create")
            else:
                logger.debug(f"Skip Plugin<{key}> on_create callback not found")

            assert module_name.startswith(prefix)
            plugins[key] = plugin

        self._plugins = plugins

    def keys(self):
        return self._plugins.keys()

    def get(self, module_name: str) -> Optional[CorePlugin]:
        return self._plugins.get(module_name, None)

    @staticmethod
    async def _close(plugins: Dict[str, CorePlugin]) -> None:
        # Use sequential 'await' for convenient debugging.
        # Therefore, you should not use the 'gather' function.
        for key, plugin in plugins.items():
            if plugin.has_on_close:
                logger.debug(f"Plugin<{key}> Calling on_close ...")
                try:
                    await plugin.on_close()
                except BaseException as e:
                    logger.exception(e)
                    # Even if an error occurs, it is forced to proceed.
                else:
                    logger.info(f"Plugin<{key}> Called on_close")
            else:
                logger.debug(f"Skip Plugin<{key}> on_close callback not found")

            if plugin.has_on_destroy:
                logger.debug(f"Plugin<{key}> Calling on_destroy ...")
                try:
                    plugin.on_destroy()
                except BaseException as e:
                    logger.exception(e)
                    # Even if an error occurs, it is forced to proceed.
                else:
                    logger.info(f"Plugin<{key}> Called on_destroy")
            else:
                logger.debug(f"Skip Plugin<{key}> on_destroy callback not found")

    async def close(self) -> None:
        await self._close(self._plugins)

    async def open(self) -> None:
        # Use sequential 'await' for convenient debugging.
        # Therefore, you should not use the 'gather' function.
        opened_plugins = dict()

        try:
            for key, plugin in self._plugins.items():
                if plugin.has_on_open:
                    logger.debug(f"Plugin<{key}> Calling on_open ...")
                    await plugin.on_open()
                    opened_plugins[key] = plugin
                    logger.info(f"Plugin<{key}> Called on_open")
                else:
                    logger.debug(f"Skip Plugin<{key}> on_open callback not found")

                if plugin.has_on_routes:
                    logger.debug(f"Plugin<{key}> Calling update_routes ...")
                    plugin.update_routes()
                    logger.info(f"Plugin<{key}> Called update_routes")
                else:
                    logger.debug(f"Skip Plugin<{key}> update_routes callback not found")
        except:  # noqa
            # [IMPORTANT]
            # If an error occurs even in one plug-in,
            # you must forcibly close all plug-ins.
            # Otherwise, critical issues may arise.
            # e.g. When a new task is executed in the plug-in,
            # the program is not terminated unless the corresponding task is terminated.
            logger.error("Aborted opening plugin !!")
            await self._close(opened_plugins)
            raise

    async def on_create_group(self, uid: int) -> None:
        coroutines = []
        for plugin in self._plugins.values():
            if plugin.has_on_create_group:
                coroutines.append(plugin.on_create_group(uid))
        await gather(*coroutines)

    async def on_delete_group(self, uid: int) -> None:
        coroutines = []
        for plugin in self._plugins.values():
            if plugin.has_on_delete_group:
                coroutines.append(plugin.on_delete_group(uid))
        await gather(*coroutines)

    async def on_create_project(self, uid: int) -> None:
        coroutines = []
        for plugin in self._plugins.values():
            if plugin.has_on_create_project:
                coroutines.append(plugin.on_create_project(uid))
        await gather(*coroutines)

    async def on_delete_project(self, uid: int) -> None:
        coroutines = []
        for plugin in self._plugins.values():
            if plugin.has_on_delete_project:
                coroutines.append(plugin.on_delete_project(uid))
        await gather(*coroutines)

    def as_answer_packet(self) -> List[PluginA]:
        return [PluginA(name=k, menus=p.spec.menus) for k, p in self._plugins.items()]
