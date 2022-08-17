# -*- coding: utf-8 -*-

from recc.plugin.mixin.plugin_create import PluginCreate
from recc.plugin.mixin.plugin_group import PluginGroup
from recc.plugin.mixin.plugin_open import PluginOpen
from recc.plugin.mixin.plugin_project import PluginProject
from recc.plugin.mixin.plugin_router import PluginRouter
from recc.plugin.mixin.plugin_spec import PluginSpec
from recc.plugin.mixin.plugin_version import PluginVersion


class CorePlugin(
    PluginCreate,
    PluginGroup,
    PluginOpen,
    PluginProject,
    PluginRouter,
    PluginSpec,
    PluginVersion,
):
    def __init__(self, module_name: str, isolate=False):
        self._module = self.import_module(module_name, isolate=isolate)
