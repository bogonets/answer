# -*- coding: utf-8 -*-

from typing import Optional, List, Any, Set, Dict, get_type_hints
from recc.core.mixin.context_base import ContextBase
from recc.event.watcher_container import WatcherContainer
from recc.packet.config import ConfigA
from recc.argparse.config.core_config import CoreConfig
from recc.logging.logging import recc_core_logger as logger
from recc.logging.logging import set_root_level
from recc.argparse.parser.env_parse import get_filtered_namespace
from recc.variables.database import CONFIG_PREFIX_RECC_ARGPARSE_CONFIG

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

    _config_watcher: WatcherContainer

    def _on_watch_log_level(self, new, old) -> None:
        assert self
        logger.info(f"Change the severity of the root logger: {old} -> {new}")
        set_root_level(new)

    def setup_context_config(self) -> None:
        self._config_watcher = WatcherContainer()
        self._config_watcher["log_level"] = self._on_watch_log_level

    async def _set_config_value(self, key: str, val: Any) -> None:
        assert self._config is not None

        if key in self._config_watcher:
            old_value = getattr(self._config, key, None)

            # Call the watcher.
            self._config_watcher.call_synced_watcher(key, val, old_value)

        # Save to database.
        info_key = CONFIG_PREFIX_RECC_ARGPARSE_CONFIG + key
        info_value = str(val)
        await self.database.upsert_info(info_key, info_value)

        # Updates the configuration in memory.
        setattr(self._config, key, val)

    async def restore_configs(self, configs: Dict[str, str]) -> None:
        assert self._config is not None

        prefix = CONFIG_PREFIX_RECC_ARGPARSE_CONFIG
        filtered_configs = get_filtered_namespace(configs, prefix)

        for key, val in vars(filtered_configs).items():
            if key in CORE_CONFIG_TYPE_HINTS:
                new_value = CORE_CONFIG_TYPE_HINTS[key](val)
            else:
                if hasattr(self._config, key):
                    new_value = type(getattr(self._config, key))(val)
                else:
                    new_value = val

            if key in self._config_watcher:
                old_value = getattr(self._config, key, None)

                # Call the watcher.
                self._config_watcher.call_synced_watcher(key, new_value, old_value)

            setattr(self._config, key, new_value)

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

    async def set_config(
        self,
        key: str,
        val: Any,
        dev_mode: Optional[bool] = None,
    ) -> None:
        keys = self.get_config_keys(dev_mode)
        if key not in keys:
            raise KeyError(f"Not exists config key: {key}")

        if key in CORE_CONFIG_TYPE_HINTS:
            cls = CORE_CONFIG_TYPE_HINTS[key]
            if issubclass(cls, bool) and isinstance(val, str):
                val_lower = val.lower()
                if val_lower == "true":
                    update_value = True
                elif val_lower == "false":
                    update_value = False
                else:
                    raise ValueError(f"Unknown boolean value: {val}")
            else:
                update_value = CORE_CONFIG_TYPE_HINTS[key](val)
            await self._set_config_value(key, update_value)
        else:
            await self._set_config_value(key, val)

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
