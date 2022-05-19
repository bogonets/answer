# -*- coding: utf-8 -*-

from asyncio import gather
from re import Pattern
from re import compile as re_compile
from typing import Dict, List, Optional, Union

from recc.logging.logging import recc_plugin_logger as logger
from recc.package.package_utils import filter_module_names as _filter_module_names
from recc.plugin.core_plugin import CorePlugin
from recc.variables.plugin import PLUGIN_PACKAGE_PREFIX


def convert_patterns(
    patterns: Optional[List[Union[str, Pattern]]] = None
) -> List[Pattern]:
    if not patterns:
        return list()

    result = list()
    for pattern in patterns:
        if isinstance(pattern, str):
            result.append(re_compile(pattern))
        elif isinstance(pattern, Pattern):
            result.append(pattern)
        else:
            raise TypeError(f"Unsupported pattern type: `{type(pattern).__name__}`")
    return result


def filter_module_names(
    filter_prefix: str,
    allow_patterns: Optional[List[Union[str, Pattern]]] = None,
    deny_patterns: Optional[List[Union[str, Pattern]]] = None,
) -> List[str]:
    allows = convert_patterns(allow_patterns)
    denies = convert_patterns(deny_patterns)
    result = list()
    for module_name in _filter_module_names(filter_prefix):
        # The deny list has high priority.
        if denies:
            for deny in denies:
                if deny.match(module_name) is not None:
                    logger.debug(
                        f"The module has been filtered by the deny list: {module_name}"
                    )
                    continue

        # If the allow list is not defined, add it forcibly.
        if not allows:
            result.append(module_name)
            continue

        for allow in allows:
            if allow.match(module_name) is not None:
                result.append(module_name)
                continue

        logger.debug(f"The module has been added by the allow list: {module_name}")

    return result


class CorePluginManager:
    def __init__(
        self,
        filter_prefix=PLUGIN_PACKAGE_PREFIX,
        context=None,
        *,
        allow_patterns: Optional[List[Union[str, Pattern]]] = None,
        deny_patterns: Optional[List[Union[str, Pattern]]] = None,
    ):
        module_names = filter_module_names(
            filter_prefix=filter_prefix,
            allow_patterns=allow_patterns,
            deny_patterns=deny_patterns,
        )

        plugins = dict()
        for module_name in module_names:
            key = module_name[len(filter_prefix) :]
            plugin = CorePlugin(module_name)
            if plugin.has_on_create:
                logger.debug(f"Plugin<{key}> Calling on_create ...")
                plugin.on_create(context=context)
                logger.info(f"Plugin<{key}> Called on_create")
            else:
                logger.debug(f"Skip Plugin<{key}> on_create callback not found")
            assert module_name.startswith(filter_prefix)
            plugins[key] = plugin
        self._plugins = plugins

    def keys(self):
        return self._plugins.keys()

    def get(self, module_name: str) -> Optional[CorePlugin]:
        return self._plugins.get(module_name, None)

    def __setitem__(self, module_name: str, plugin: CorePlugin) -> None:
        self._plugins.__setitem__(module_name, plugin)

    def __getitem__(self, module_name: str) -> CorePlugin:
        return self._plugins.__getitem__(module_name)

    def __delitem__(self, module_name: str) -> None:
        self._plugins.__delitem__(module_name)

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

    async def call_on_create_group(self, uid: int) -> None:
        coroutines = []
        for plugin in self._plugins.values():
            if plugin.has_on_create_group:
                coroutines.append(plugin.on_create_group(uid))
        await gather(*coroutines)

    async def call_on_delete_group(self, uid: int) -> None:
        coroutines = []
        for plugin in self._plugins.values():
            if plugin.has_on_delete_group:
                coroutines.append(plugin.on_delete_group(uid))
        await gather(*coroutines)

    async def call_on_create_project(self, uid: int) -> None:
        coroutines = []
        for plugin in self._plugins.values():
            if plugin.has_on_create_project:
                coroutines.append(plugin.on_create_project(uid))
        await gather(*coroutines)

    async def call_on_delete_project(self, uid: int) -> None:
        coroutines = []
        for plugin in self._plugins.values():
            if plugin.has_on_delete_project:
                coroutines.append(plugin.on_delete_project(uid))
        await gather(*coroutines)
