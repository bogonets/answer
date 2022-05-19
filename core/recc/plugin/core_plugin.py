# -*- coding: utf-8 -*-

from recc.plugin.mixin.plugin_create import PluginCreate
from recc.plugin.mixin.plugin_group import PluginGroup
from recc.plugin.mixin.plugin_open import PluginOpen
from recc.plugin.mixin.plugin_project import PluginProject
from recc.plugin.mixin.plugin_router import PluginRouter
from recc.plugin.mixin.plugin_www import PluginWww


class CorePlugin(
    PluginCreate,
    PluginGroup,
    PluginOpen,
    PluginProject,
    PluginRouter,
    PluginWww,
):
    def __init__(self, module_name: str):
        self._module = self.import_module(module_name)
        self._routes = list()
