# -*- coding: utf-8 -*-

import os
import sys
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    FATAL,
    INFO,
    NOTSET,
    WARN,
    WARNING,
    Formatter,
    Logger,
    StreamHandler,
)
from logging import config as logging_config
from logging import getLogger
from typing import Final, Literal, Optional, Union

LOGGER_NAME_RECC = "recc"
LOGGER_NAME_RECC_CORE = "recc.core"
LOGGER_NAME_RECC_HTTP = "recc.http"
LOGGER_NAME_RECC_PLUGIN = "recc.plugin"

recc_logger = getLogger(LOGGER_NAME_RECC)
recc_core_logger = getLogger(LOGGER_NAME_RECC_CORE)
recc_http_logger = getLogger(LOGGER_NAME_RECC_HTTP)
recc_plugin_logger = getLogger(LOGGER_NAME_RECC_PLUGIN)

SEVERITY_NAME_CRITICAL = "critical"
SEVERITY_NAME_FATAL = "fatal"
SEVERITY_NAME_ERROR = "error"
SEVERITY_NAME_WARNING = "warning"
SEVERITY_NAME_WARN = "warn"
SEVERITY_NAME_INFO = "info"
SEVERITY_NAME_DEBUG = "debug"
SEVERITY_NAME_NOTSET = "notset"
SEVERITY_NAME_OFF = "off"

SEVERITIES = (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_FATAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_WARN,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)

LoggingStyleLiteral = Literal["%", "{", "$"]

DEFAULT_SIMPLE_LOGGING_FORMAT: Final[str] = "{levelname[0]} [{name}] {message}"
DEFAULT_SIMPLE_LOGGING_STYLE: Final[LoggingStyleLiteral] = "{"


def get_logger(logger: Optional[Union[str, Logger]] = None) -> Logger:
    if logger is None:
        return recc_logger
    if isinstance(logger, str):
        return getLogger(logger)
    elif isinstance(logger, Logger):
        return logger
    else:
        raise TypeError(f"Unsupported logger type: {type(logger).__name__}")


def convert_level_number(level: Optional[Union[str, int]] = None) -> int:
    if level is None:
        return DEBUG

    if isinstance(level, str):
        ll = level.lower()
        if ll == SEVERITY_NAME_CRITICAL:
            return CRITICAL
        elif ll == SEVERITY_NAME_FATAL:
            return FATAL
        elif ll == SEVERITY_NAME_ERROR:
            return ERROR
        elif ll == SEVERITY_NAME_WARNING:
            return WARNING
        elif ll == SEVERITY_NAME_WARN:
            return WARN
        elif ll == SEVERITY_NAME_INFO:
            return INFO
        elif ll == SEVERITY_NAME_DEBUG:
            return DEBUG
        elif ll == SEVERITY_NAME_NOTSET:
            return NOTSET
        elif ll == SEVERITY_NAME_OFF:
            return CRITICAL + 100
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
        if level > CRITICAL:
            return "OverCritical"
        if level == CRITICAL:
            return "Critical"
        if level > ERROR:
            return "OverError"
        if level == ERROR:
            return "Error"
        if level > WARNING:
            return "OverWarning"
        if level == WARNING:
            return "Warning"
        if level > INFO:
            return "OverInfo"
        if level == INFO:
            return "Info"
        if level > DEBUG:
            return "OverDebug"
        if level == DEBUG:
            return "Debug"
        if level > NOTSET:
            return "OverNotSet"
        if level == NOTSET:
            return "NotSet"
    return str(level)


def set_root_level(level: Union[str, int]) -> None:
    getLogger().setLevel(convert_level_number(level))


def set_basic_config(config_file: str) -> None:
    assert os.path.isfile(config_file)

    ext = os.path.splitext(config_file)[1].lower()
    if ext == ".json":
        import json

        with open(config_file, "r") as f:
            logging_config.dictConfig(json.loads(f.read()))
    elif ext in (".yml", "yaml"):
        import yaml

        with open(config_file, "r") as f:
            logging_config.dictConfig(yaml.full_load(f.read()))
    else:
        logging_config.fileConfig(config_file)


def get_root_level() -> int:
    return getLogger().level


FMT_TIME = "%(asctime)s.%(msecs)03d"
FMT_THREAD = "%(process)d/%(thread)s"

DEFAULT_FORMAT = f"{FMT_TIME} {FMT_THREAD} %(name)s %(levelname)s %(message)s"
DEFAULT_DATEFMT = "%Y-%m-%d %H:%M:%S"
DEFAULT_STYLE = "%"

SIMPLE_FORMAT = "{levelname[0]} {asctime} {name} {message}"
SIMPLE_DATEFMT = "%Y%m%d %H%M%S"
SIMPLE_STYLE = "{"

DEFAULT_LOGGING_CONFIG = {
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
            "class": "recc.logging.colored_formatter.ColoredFormatter",
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
        "file_default": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": "recc.log",
            "mode": "a",
            "encoding": "utf-8",
            "delay": False,
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console_color"],
            "level": "DEBUG",
        },
        "zeep": {
            "level": "WARNING",
        },
        "aiortc": {
            "level": "ERROR",
        },
        "aioice": {
            "level": "ERROR",
        },
        "matplotlib": {
            "level": "INFO",
        },
    },
}


def set_default_logging_config() -> None:
    logging_config.dictConfig(DEFAULT_LOGGING_CONFIG)


def set_simple_logging_config() -> None:
    simple_formatter = Formatter(
        fmt=DEFAULT_SIMPLE_LOGGING_FORMAT,
        style=DEFAULT_SIMPLE_LOGGING_STYLE,
    )
    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setFormatter(simple_formatter)
    root_logger = getLogger()
    root_logger.addHandler(stream_handler)
    root_logger.setLevel(DEBUG)
