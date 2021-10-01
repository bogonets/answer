# -*- coding: utf-8 -*-

from typing import List, Any, get_type_hints
from recc.core.mixin.context_base import ContextBase
from recc.packet.config import ConfigA
from recc.argparse.config.core_config import CoreConfig

IGNORE_CONFIG_KEYS = {
    "command",
    "version",
    "help",
    "help_message",
    "unrecognized_arguments",
}
CORE_CONFIG_TYPE_HINTS = get_type_hints(CoreConfig)
CONFIG_TYPES = {
    k: v for k, v in CORE_CONFIG_TYPE_HINTS.items() if k not in IGNORE_CONFIG_KEYS
}


class ContextConfig(ContextBase):
    def get_config_keys(self) -> List[str]:
        return list(
            filter(
                lambda x: x not in IGNORE_CONFIG_KEYS,
                vars(self.config).keys(),
            )
        )

    def set_config(self, key: str, val: Any) -> None:
        if key in CONFIG_TYPES:
            setattr(self.config, key, CONFIG_TYPES[key](val))
        else:
            setattr(self.config, key, val)

    def get_configs(self) -> List[ConfigA]:
        result = list()
        for key in self.get_config_keys():
            value = getattr(self.config, key)
            if key in CONFIG_TYPES:
                type_name = CONFIG_TYPES[key].__name__
            else:
                type_name = type(value).__name__
            result.append(ConfigA(key, type_name, str(value)))
        return result

    def get_config(self, key: str) -> ConfigA:
        if key not in self.get_config_keys():
            raise KeyError(f"Not exists {key} key")
        value = getattr(self.config, key)
        if key in CONFIG_TYPES:
            type_name = CONFIG_TYPES[key].__name__
        else:
            type_name = type(value).__name__
        return ConfigA(key, type_name, str(value))
