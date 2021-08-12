# -*- coding: utf-8 -*-

from typing import List, Any, get_type_hints
from recc.core.mixin.context_base import ContextBase
from recc.core.struct.config import Config
from recc.argparse.config.core_config import CoreConfig

_CORE_CONFIG_TYPE_HINTS = get_type_hints(CoreConfig)

CONFIG_KEYS = [
    "manage_port_min",
    "manage_port_max",
    "signature",
    "public_signup",
    "access_token_duration",
    "refresh_token_duration",
]
CONFIG_TYPES = {k: _CORE_CONFIG_TYPE_HINTS[k] for k in CONFIG_KEYS}


class ContextConfig(ContextBase):
    def update_config(self, key: str, val: Any) -> None:
        setattr(self.config, key, CONFIG_TYPES[key](val))

    def get_config_keys(self) -> List[str]:
        assert self is not None
        return CONFIG_KEYS

    def get_configs(self) -> List[Config]:
        result = list()
        for key in CONFIG_KEYS:
            type_name = CONFIG_TYPES[key].__name__
            value = getattr(self.config, key)
            result.append(Config(key, type_name, str(value)))
        return result

    def get_config(self, key: str) -> Config:
        if key not in CONFIG_KEYS:
            raise KeyError(f"Not exists {key} key")
        type_name = CONFIG_TYPES[key].__name__
        value = getattr(self.config, key)
        return Config(key, type_name, str(value))
