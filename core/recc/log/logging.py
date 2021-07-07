# -*- coding: utf-8 -*-

import os
import logging
from logging import config as logging_config
from typing import Union

LOGGER_NAME_RECC = "recc"
LOGGER_NAME_CORE_RECC = "recc.core"
LOGGER_NAME_RECC_HTTP = "recc.http"
LOGGER_NAME_RECC_RPC = "recc.rpc"
LOGGER_NAME_RECC_CONTAINER = "recc.container"
LOGGER_NAME_RECC_CACHE = "recc.cache"
LOGGER_NAME_RECC_DATABASE = "recc.database"
LOGGER_NAME_RECC_COMMON = "recc.common"

recc_logger = logging.getLogger(LOGGER_NAME_RECC)
recc_core_logger = logging.getLogger(LOGGER_NAME_CORE_RECC)
recc_http_logger = logging.getLogger(LOGGER_NAME_RECC_HTTP)
recc_rpc_logger = logging.getLogger(LOGGER_NAME_RECC_RPC)
recc_container_logger = logging.getLogger(LOGGER_NAME_RECC_CONTAINER)
recc_cache_logger = logging.getLogger(LOGGER_NAME_RECC_CACHE)
recc_database_logger = logging.getLogger(LOGGER_NAME_RECC_DATABASE)
recc_common_logger = logging.getLogger(LOGGER_NAME_RECC_COMMON)

SEVERITY_NAME_CRITICAL = "critical"
SEVERITY_NAME_FATAL = "fatal"
SEVERITY_NAME_ERROR = "error"
SEVERITY_NAME_WARNING = "warning"
SEVERITY_NAME_WARN = "warn"
SEVERITY_NAME_INFO = "info"
SEVERITY_NAME_DEBUG = "debug"
SEVERITY_NAME_NOTSET = "notset"
SEVERITY_NAME_OFF = "off"


def convert_level_number(level: Union[str, int]) -> int:
    if isinstance(level, str):
        ll = level.lower()
        if ll == SEVERITY_NAME_CRITICAL:
            return logging.CRITICAL
        elif ll == SEVERITY_NAME_FATAL:
            return logging.FATAL
        elif ll == SEVERITY_NAME_ERROR:
            return logging.ERROR
        elif ll == SEVERITY_NAME_WARNING:
            return logging.WARNING
        elif ll == SEVERITY_NAME_WARN:
            return logging.WARN
        elif ll == SEVERITY_NAME_INFO:
            return logging.INFO
        elif ll == SEVERITY_NAME_DEBUG:
            return logging.DEBUG
        elif ll == SEVERITY_NAME_NOTSET:
            return logging.NOTSET
        elif ll == SEVERITY_NAME_OFF:
            return logging.CRITICAL + 100
        else:
            try:
                return int(ll)
            except ValueError:
                raise ValueError(f"Unknown level: {level}")
    elif isinstance(level, int):
        return level
    else:
        raise TypeError(f"Unsupported level type: {type(level)}")


def convert_printable_level(level: Union[str, int]) -> str:
    if isinstance(level, str):
        return level
    if isinstance(level, int):
        if level > logging.CRITICAL:
            return "OverCritical"
        if level == logging.CRITICAL:
            return "Critical"
        if level > logging.ERROR:
            return "OverError"
        if level == logging.ERROR:
            return "Error"
        if level > logging.WARNING:
            return "OverWarning"
        if level == logging.WARNING:
            return "Warning"
        if level > logging.INFO:
            return "OverInfo"
        if level == logging.INFO:
            return "Info"
        if level > logging.DEBUG:
            return "OverDebug"
        if level == logging.DEBUG:
            return "Debug"
        if level > logging.NOTSET:
            return "OverNotSet"
        if level == logging.NOTSET:
            return "NotSet"
    return str(level)


def set_root_level(level: Union[str, int]) -> None:
    logging.getLogger().setLevel(convert_level_number(level))


def set_basic_config(config_file: str) -> None:
    assert os.path.isfile(config_file)

    ext = os.path.splitext(config_file)[1].lower()
    if ext == ".json":
        import json

        with open(config_file, "r") as f:
            logging_config.dictConfig(json.loads(f.read()))
    elif ext == ".yml" or ext == ".yaml":
        import yaml

        with open(config_file, "r") as f:
            logging_config.dictConfig(yaml.full_load(f.read()))
    else:
        logging_config.fileConfig(config_file)


def get_root_level() -> int:
    return logging.getLogger().level


_FMT_TIME = "%(asctime)s.%(msecs)03d"
_FMT_THREAD = "%(process)d/%(thread)s"

DEFAULT_FORMAT = f"{_FMT_TIME} {_FMT_THREAD} %(name)s %(levelname)s %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"
DEFAULT_STYLE = "%"

SIMPLE_FORMAT = "{levelname[0]} {asctime} {name} {message}"
SIMPLE_DATEFMT = "%Y%m%d %H%M%S"
SIMPLE_STYLE = "{"

_DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_DATEFMT,
            "style": DEFAULT_STYLE,
        },
        "simple": {
            "format": SIMPLE_FORMAT,
            "datefmt": SIMPLE_DATEFMT,
            "style": SIMPLE_STYLE,
        },
        "color": {
            "class": "recc.log.colored_formatter.ColoredFormatter",
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_DATEFMT,
            "style": DEFAULT_STYLE,
        },
    },
    "handlers": {
        "console_default": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "console_simple": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "console_color": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "color",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console_color"],
            "level": "DEBUG",
        },
        "aiohttp": {
            "level": "DEBUG",
        },
        "asyncio": {
            "level": "DEBUG",
        },
        "docker": {
            "level": "DEBUG",
        },
        "elasticsearch": {
            "level": "DEBUG",
        },
        "grpc": {
            "level": "DEBUG",
        },
        LOGGER_NAME_RECC: {
            "level": "DEBUG",
        },
        "urllib3": {
            "level": "DEBUG",
        },
    },
}


def set_default_logging_config() -> None:
    logging_config.dictConfig(_DEFAULT_LOGGING_CONFIG)
