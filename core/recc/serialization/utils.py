# -*- coding: utf-8 -*-

from typing import Any, Dict


def update_dict(
    result: Dict[str, Any],
    key: str,
    value: Any,
    default: Any = None,
) -> None:
    if value is None:
        if default is not None:
            result[key] = default
    else:
        result[key] = value
