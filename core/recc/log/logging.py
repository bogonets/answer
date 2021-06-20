# -*- coding: utf-8 -*-

import os
import logging
from logging import config as logging_config
from typing import Union

LOGGER_NAME_RECC = "recc"
LOGGER_NAME_RECC_HTTP = "recc.http"
LOGGER_NAME_RECC_RPC = "recc.rpc"
LOGGER_NAME_RECC_CM = "recc.cm"
LOGGER_NAME_RECC_CS = "recc.cs"
LOGGER_NAME_RECC_DB = "recc.db"
LOGGER_NAME_RECC_STORAGE = "recc.storage"

recc_logger = logging.getLogger(LOGGER_NAME_RECC)
recc_http_logger = logging.getLogger(LOGGER_NAME_RECC_HTTP)
recc_rpc_logger = logging.getLogger(LOGGER_NAME_RECC_RPC)
recc_cm_logger = logging.getLogger(LOGGER_NAME_RECC_CM)
recc_cs_logger = logging.getLogger(LOGGER_NAME_RECC_CS)
recc_db_logger = logging.getLogger(LOGGER_NAME_RECC_DB)
recc_storage_logger = logging.getLogger(LOGGER_NAME_RECC_STORAGE)

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


DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname[0]} {asctime} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "aiohttp.access": {
            "level": "DEBUG",
        },
        "aiohttp.client": {
            "level": "DEBUG",
        },
        "aiohttp.internal": {
            "level": "DEBUG",
        },
        "aiohttp.server": {
            "level": "DEBUG",
        },
        "aiohttp.web": {
            "level": "DEBUG",
        },
        "aiohttp.websocket": {
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
        LOGGER_NAME_RECC: {
            "level": "DEBUG",
        },
        LOGGER_NAME_RECC_HTTP: {
            "level": "DEBUG",
        },
        LOGGER_NAME_RECC_RPC: {
            "level": "DEBUG",
        },
        LOGGER_NAME_RECC_CM: {
            "level": "DEBUG",
        },
        LOGGER_NAME_RECC_CS: {
            "level": "DEBUG",
        },
        LOGGER_NAME_RECC_DB: {
            "level": "DEBUG",
        },
        "docker.auth": {
            "level": "DEBUG",
        },
        "docker.utils.config": {
            "level": "DEBUG",
        },
        "urllib3.connectionpool": {
            "level": "DEBUG",
        },
    },
}


def set_default_logging_config() -> None:
    logging_config.dictConfig(DEFAULT_LOGGING_CONFIG)
