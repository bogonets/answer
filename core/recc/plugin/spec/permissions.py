# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from recc.variables.plugin import SPEC_PERMISSIONS


def parse_spec_permissions(spec: Dict[str, Any]) -> List[str]:
    if SPEC_PERMISSIONS not in spec:
        return list()

    permissions = spec[SPEC_PERMISSIONS]
    if not isinstance(permissions, (tuple, list, set)):
        typename = type(permissions).__name__
        raise TypeError(f"Unsupported `{SPEC_PERMISSIONS}` type: {typename}")

    result = list()
    for permission in permissions:
        if not isinstance(permission, str):
            typename = type(permission).__name__
            raise TypeError(f"Permission `elements` must be of type 'str': {typename}")
        result.append(permission)

    return result
