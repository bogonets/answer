# -*- coding: utf-8 -*-

from typing import Optional

from recc.filesystem.permission import is_readable_file
from recc.logging.logging import convert_printable_level
from recc.logging.logging import recc_common_logger as logger
from recc.logging.logging import (
    set_basic_config,
    set_default_logging_config,
    set_root_level,
    set_simple_logging_config,
)


def init_logger(
    config_path: str,
    log_level: Optional[str] = None,
    simply=False,
) -> None:
    log_configurable: bool
    if simply:
        log_configurable = False
        set_simple_logging_config()
    else:
        log_configurable = bool(config_path and is_readable_file(config_path))
        if log_configurable:
            set_basic_config(config_path)
        else:
            set_default_logging_config()

    if log_level:
        set_root_level(log_level)

    # The resulting output should be after the logger setup is done.
    if log_configurable:
        logger.info(f"Initialize log config: {config_path}")
    if log_level:
        logger.info(f"Change root log level: {convert_printable_level(log_level)}")
