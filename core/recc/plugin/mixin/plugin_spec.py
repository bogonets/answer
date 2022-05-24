# -*- coding: utf-8 -*-

import os
from typing import Any, Dict, List, Optional

from recc.plugin.errors import PluginAttributeInvalidValueError
from recc.plugin.mixin._plugin_base import PluginBase
from recc.regex.resource_matcher import MatchItem, find_match_file
from recc.variables.plugin import (
    NAME_RECC_SPEC,
    SPEC_WWW,
    STATIC_WEB_FILES_DIRECTORY_NAME,
)


def parse_spec_www(spec: Dict[str, Any]) -> List[MatchItem]:
    if SPEC_WWW not in spec:
        return list()

    www = spec[SPEC_WWW]
    if not isinstance(www, (tuple, list, set)):
        raise TypeError(f"Unsupported www type: {type(www).__name__}")

    return [MatchItem.parse(item) for item in www]


class ReccSpec:
    def __init__(self, spec: Optional[Dict[str, Any]] = None):
        self._spec: Dict[str, Any] = spec if spec else dict()
        self._www = parse_spec_www(self._spec)

    def match_www(self, base_dir: str, test_value: str) -> str:
        return os.path.join(base_dir, find_match_file(self._www, test_value, base_dir))


class PluginSpec(PluginBase):

    _recc_spec: Optional[ReccSpec] = None

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
        return self.spec.match_www(self.www_dir, test_value)
