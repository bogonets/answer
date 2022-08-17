# -*- coding: utf-8 -*-

import os
from typing import Any, Dict, Optional

from recc.plugin.errors import PluginAttributeInvalidValueError
from recc.plugin.mixin._plugin_base import PluginBase
from recc.plugin.spec.menus import parse_spec_menus
from recc.plugin.spec.permissions import parse_spec_permissions
from recc.plugin.spec.www import parse_spec_www
from recc.regex.resource_matcher import find_match_file
from recc.variables.plugin import NAME_RECC_SPEC, STATIC_WEB_FILES_DIRECTORY_NAME


class ReccSpec:
    def __init__(self, spec: Optional[Dict[str, Any]] = None):
        self.raw: Dict[str, Any] = spec if spec else dict()
        self.menus = parse_spec_menus(self.raw)
        self.permissions = parse_spec_permissions(self.raw)
        self.www = parse_spec_www(self.raw)


class PluginSpec(PluginBase):

    _recc_spec: Optional[ReccSpec]

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._recc_spec = None
        return instance

    @property
    def spec(self) -> ReccSpec:
        if self._recc_spec is not None:
            return self._recc_spec

        if not self.has(NAME_RECC_SPEC):
            return ReccSpec()

        value = self.get(NAME_RECC_SPEC)

        if value is None:
            return ReccSpec()

        if not isinstance(value, dict):
            raise PluginAttributeInvalidValueError(
                self.module_name,
                NAME_RECC_SPEC,
                "The attribute must be of type `dict`",
            )

        self._recc_spec = ReccSpec(value)
        return self._recc_spec

    @property
    def www_dir(self) -> str:
        return os.path.join(self.module_directory, STATIC_WEB_FILES_DIRECTORY_NAME)

    def match_www(self, test_value: str) -> str:
        base_dir = self.www_dir
        matches = self.spec.www
        filename = find_match_file(matches, test_value, base_dir)
        return os.path.join(self.www_dir, filename)
