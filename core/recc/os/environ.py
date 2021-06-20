# -*- coding: utf-8 -*-

from os import environ
from typing import Optional, Dict, Any, Type


def get_os_envs_dict() -> Dict[str, str]:
    return {k: str(environ.get(k)) for k in environ if environ}


def exchange_env(key: str, exchange: Optional[str]) -> Optional[str]:
    result = environ.get(key)
    if result is not None:
        environ.pop(key)
    if exchange is not None:
        environ[key] = exchange
    return result


def get_env(key: str) -> Optional[str]:
    return environ.get(key)


def opt_env(key: str, default_value: Any, result_class: Type) -> Any:
    value = environ.get(key)
    if value is None:
        return default_value
    try:
        return result_class(value)
    except ValueError:
        return default_value
