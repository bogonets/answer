# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
from re import Pattern
from typing import Any, Dict, List, Optional

from recc.plugin.errors import PluginAttributeInvalidValueError
from recc.plugin.mixin._plugin_base import PluginBase
from recc.regex.access_filter import compile_pattern
from recc.variables.plugin import (
    NAME_RECC_SPEC,
    SPEC_WWW,
    STATIC_WEB_FILES_DIRECTORY_NAME,
)


@dataclass
class ReccSpecWww:
    pattern: Pattern
    file: str


def _parse_spec_www(spec: Dict[str, Any]) -> List[ReccSpecWww]:
    if SPEC_WWW not in spec:
        return list()

    www = spec[SPEC_WWW]
    assert isinstance(www, list)

    result = list()
    for item in www:
        assert isinstance(item, tuple)
        assert len(item) == 2

        pattern = compile_pattern(item[0])
        file = item[1]
        assert isinstance(file, str)

        result.append(ReccSpecWww(pattern, file))

    return result


class ReccSpec:
    def __init__(self, spec: Optional[Dict[str, Any]] = None):
        self._spec: Dict[str, Any] = spec if spec else dict()
        self._www = _parse_spec_www(self._spec)

    def match_www(self, path: str) -> str:
        for www in self._www:
            if www.pattern.match(path) is not None:
                return www.file
        raise KeyError("No matching www resource was found")


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

    def match_www(self, path: str) -> str:
        return os.path.join(self.www_dir, self.spec.match_www(path))
