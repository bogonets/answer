# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional, Set, get_origin, get_type_hints

from generalize_config.parser.env_parse import filter_dict

from recc.aio.watcher_container import WatcherContainer
from recc.config import Config
from recc.core.mixin.context_base import ContextBase
from recc.logging.logging import recc_core_logger as logger
from recc.logging.logging import set_root_level
from recc.packet.config import ConfigA
from recc.variables.database import CONFIG_PREFIX_RECC_ARGPARSE_CONFIG

IGNORE_CONFIG_KEYS = {
    "command",
    "version",
    "help",
    "help_message",
    "unrecognized_arguments",
}
CORE_CONFIG_TYPE_HINTS = get_type_hints(Config)


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
        """
        It is used to restore configurations changed by the user at runtime.
        """
        assert self._config is not None

        prefix = CONFIG_PREFIX_RECC_ARGPARSE_CONFIG
        filtered_configs = filter_dict(configs, prefix=prefix)

        for key, val in filtered_configs.items():
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
        return set(Config.release_keys())

    def get_develop_config_keys(self) -> Set[str]:
        return set(
            filter(
                lambda x: x not in IGNORE_CONFIG_KEYS,
                vars(self._config).keys(),
            )
        )

    def get_config_keys(self, *, dev_mode: Optional[bool] = None) -> Set[str]:
        if dev_mode is None:
            # MUST be specified to avoid 'ambiguous' calls.
            raise ValueError("The `dev_mode` argument must be specified")

        if self._config.developer if dev_mode is None else dev_mode:
            return self.get_develop_config_keys()
        else:
            return self.get_release_config_keys()

    async def set_config(self, key: str, val: Any) -> None:
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

    def get_configs(self, *, dev_mode: Optional[bool] = None) -> List[ConfigA]:
        if dev_mode is None:
            # MUST be specified to avoid 'ambiguous' calls.
            raise ValueError("The `dev_mode` argument must be specified")

        return [self.get_config(k) for k in self.get_config_keys(dev_mode=dev_mode)]

    def has_configs(self, key: str, *, dev_mode: Optional[bool] = None) -> bool:
        if dev_mode is None:
            # MUST be specified to avoid 'ambiguous' calls.
            raise ValueError("The `dev_mode` argument must be specified")

        return key in self.get_config_keys(dev_mode=dev_mode)

    def get_config(self, key: str) -> ConfigA:
        value = getattr(self._config, key)
        if key in CORE_CONFIG_TYPE_HINTS:
            type_origin = get_origin(CORE_CONFIG_TYPE_HINTS[key])
            if type_origin is None:
                type_name = CORE_CONFIG_TYPE_HINTS[key].__name__
            else:
                type_name = type_origin.__name__
        else:
            type_name = type(value).__name__
        return ConfigA(key, type_name, str(value))
