# -*- coding: utf-8 -*-
from typing import Optional


class PluginError(Exception):
    def __init__(self, plugin: str, *args: str):
        super().__init__(*args)
        self.plugin = plugin


# ---------------
# Attribute Error
# ---------------


class PluginAttributeError(PluginError):
    def __init__(self, plugin: str, attribute: str, detail: str):
        super().__init__(plugin, f"Plugin[{plugin}.{attribute}] {detail}")
        self.attribute = attribute


class PluginAttributeNotFoundError(PluginAttributeError):
    def __init__(self, plugin: str, attribute: str):
        super().__init__(plugin, attribute, "Attribute not found")


class PluginAttributeInvalidValueError(PluginAttributeError):
    def __init__(self, plugin: str, attribute: str, detail: Optional[str] = None):
        prefix = "The attribute value is invalid"
        message = f"{prefix}: {detail}" if detail else prefix
        super().__init__(plugin, attribute, message)


# --------------
# Callback Error
# --------------


class PluginCallbackError(PluginError):
    def __init__(self, plugin: str, callback: str, detail: str):
        super().__init__(plugin, f"Plugin[{plugin}.{callback}] {detail}")
        self.callback = callback


class PluginCallbackInvalidStateError(PluginCallbackError):
    def __init__(self, plugin: str, callback: str, detail: Optional[str] = None):
        prefix = "Invalid state"
        message = f"{prefix}: {detail}" if detail else prefix
        super().__init__(plugin, callback, message)


class PluginCallbackNotFoundError(PluginCallbackError):
    def __init__(self, plugin: str, callback: str):
        super().__init__(plugin, callback, "Callback not found")


class PluginCallbackNotCoroutineError(PluginCallbackError):
    def __init__(self, plugin: str, callback: str):
        super().__init__(plugin, callback, "The callback must be a coroutine")


class PluginCallbackCoroutineError(PluginCallbackError):
    def __init__(self, plugin: str, callback: str):
        super().__init__(plugin, callback, "The callback must not be a coroutine")


class PluginCallbackRuntimeError(PluginCallbackError):
    def __init__(self, plugin: str, callback: str):
        super().__init__(plugin, callback, "A runtime error occurred in the callback")


class PluginCallbackInvalidReturnValueError(PluginCallbackError):
    def __init__(self, plugin: str, callback: str, detail: Optional[str] = None):
        prefix = "The return value of the callback is invalid"
        message = f"{prefix}: {detail}" if detail else prefix
        super().__init__(plugin, callback, message)


class PluginCallbackNotFoundRouteError(PluginCallbackError):
    def __init__(self, plugin: str, callback: str, method: str, path: str):
        message = f"Not found route: method='{method}', path='{path}'"
        super().__init__(plugin, callback, message)


class PluginCallbackRouteRuntimeError(PluginCallbackError):
    def __init__(self, plugin: str, callback: str, method: str, path: str):
        prefix = "A runtime error occurred in the route"
        message = f"{prefix}: method='{method}', path='{path}'"
        super().__init__(plugin, callback, message)
