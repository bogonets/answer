# -*- coding: utf-8 -*-

from typing import Optional, List, Any, Set, get_type_hints
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
RELEASE_CONFIG_KEYS = {
    "user",
    "group",
    "log_level",
    "verbose",
    "external_host",
    "http_timeout",
    "public_signup",
    "access_token_duration",
    "refresh_token_duration",
}
CORE_CONFIG_TYPE_HINTS = get_type_hints(CoreConfig)


class ContextConfig(ContextBase):
    @staticmethod
    def get_release_config_keys() -> Set[str]:
        return RELEASE_CONFIG_KEYS

    def get_develop_config_keys(self) -> Set[str]:
        return set(
            filter(
                lambda x: x not in IGNORE_CONFIG_KEYS,
                vars(self.config).keys(),
            )
        )

    def get_config_keys(self, dev_mode: Optional[bool] = None) -> Set[str]:
        if dev_mode is None:
            develop = self.config.developer
        else:
            develop = dev_mode

        if develop:
            return self.get_develop_config_keys()
        else:
            return self.get_release_config_keys()

    def set_config(self, key: str, val: Any, dev_mode: Optional[bool] = None) -> None:
        keys = self.get_config_keys(dev_mode)
        if key not in keys:
            raise KeyError(f"Not exists config key: {key}")

        if key in CORE_CONFIG_TYPE_HINTS:
            cls = CORE_CONFIG_TYPE_HINTS[key]
            if issubclass(cls, bool) and isinstance(val, str):
                if val == "True":
                    update_value = True
                elif val == "False":
                    update_value = False
                else:
                    raise ValueError(f"Unknown boolean value: {val}")
            else:
                update_value = CORE_CONFIG_TYPE_HINTS[key](val)
            setattr(self._config, key, update_value)
        else:
            setattr(self._config, key, val)

    def get_configs(self, dev_mode: Optional[bool] = None) -> List[ConfigA]:
        result = list()
        for key in self.get_config_keys(dev_mode):
            value = getattr(self.config, key)
            if key in CORE_CONFIG_TYPE_HINTS:
                type_name = CORE_CONFIG_TYPE_HINTS[key].__name__
            else:
                type_name = type(value).__name__
            result.append(ConfigA(key, type_name, str(value)))
        return result

    def get_config(self, key: str, dev_mode: Optional[bool] = None) -> ConfigA:
        if key not in self.get_config_keys(dev_mode):
            raise KeyError(f"Not exists {key} key")
        value = getattr(self.config, key)
        if key in CORE_CONFIG_TYPE_HINTS:
            type_name = CORE_CONFIG_TYPE_HINTS[key].__name__
        else:
            type_name = type(value).__name__
        return ConfigA(key, type_name, str(value))
