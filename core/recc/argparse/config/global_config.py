# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser, Namespace
from typing import Iterable, Tuple, List, Optional, Any, get_type_hints
from recc.argparse.argument import Shortcut, Argument
from recc.log.logging import (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)

LOOP_DRIVER_AIO = "aio"
LOOP_DRIVER_UV = "uv"

JSON_DRIVER_JSON = "json"
JSON_DRIVER_ORJSON = "orjson"

LOG_LEVELS = (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)


class GlobalConfig(Namespace):

    command: str
    config: str
    version: bool
    help: bool

    user: str
    group: str

    log_config: str
    log_level: str

    loop_driver: str
    json_driver: str

    suppress_print: bool
    verbose: int
    teardown: bool
    developer: bool

    help_message: str
    unrecognized_arguments: List[str]


ARG_COMMAND = Argument(
    key="command",
    last_injection_value="",
    nargs="?",
    help="The command to be executed.",
)
ARG_CONFIG = Argument(
    key="--config",
    last_injection_value="",
    shortcut=Shortcut.c,
    metavar="file",
    help="Use the given config file.",
)
ARG_VERSION = Argument(
    key="--version",
    last_injection_value=False,
    default=False,
    action="store_true",
    help="Print the version number and exit.",
)
ARG_HELP = Argument(
    key="--help",
    last_injection_value=False,
    shortcut=Shortcut.h,
    default=False,
    action="store_true",
    help="Print help message.",
)

ARG_USER = Argument(
    key="--user",
    last_injection_value="recc",
    help="User name",
)
ARG_GROUP = Argument(
    key="--group",
    last_injection_value="recc",
    help="Group name",
)

ARG_LOG_CONFIG = Argument(
    key="--log-config",
    last_injection_value="logging.yml",
    help="Reads the logging configuration from a format file.",
)
ARG_LOG_LEVEL = Argument(
    key="--log-level",
    last_injection_value="",
    choices=LOG_LEVELS,
    help="Root logger severity. This value is set after configuring the log.",
)

ARG_LOOP_DRIVER = Argument(
    key="--loop-driver",
    last_injection_value=LOOP_DRIVER_AIO,
    metavar="file",
    choices=(LOOP_DRIVER_AIO, LOOP_DRIVER_UV),
    help="Async loop driver.",
)
ARG_JSON_DRIVER = Argument(
    key="--json-driver",
    last_injection_value=JSON_DRIVER_ORJSON,
    metavar="level",
    choices=(JSON_DRIVER_JSON, JSON_DRIVER_ORJSON),
    help="JSON encoder/decoder driver.",
)

ARG_SUPPRESS_PRINT = Argument(
    key="--suppress-print",
    last_injection_value=False,
    action="store_true",
    help="Suppress printing.",
)
ARG_VERBOSE = Argument(
    key="--verbose",
    last_injection_value=0,
    shortcut=Shortcut.v,
    default=0,
    action="count",
    help="Be more verbose/talkative during the operation.",
)
ARG_TEARDOWN = Argument(
    key="--teardown",
    last_injection_value=False,
    action="store_true",
    help="When the server is shut down, all resources created are released.",
)
ARG_DEVELOPER = Argument(
    key="--developer",
    last_injection_value=False,
    shortcut=Shortcut.d,
    action="store_true",
    help="Developer mode.",
)

GLOBAL_ARGS = (
    ARG_COMMAND,
    ARG_CONFIG,
    ARG_VERSION,
    ARG_HELP,
    ARG_USER,
    ARG_GROUP,
    ARG_LOG_CONFIG,
    ARG_LOG_LEVEL,
    ARG_LOOP_DRIVER,
    ARG_JSON_DRIVER,
    ARG_SUPPRESS_PRINT,
    ARG_VERBOSE,
    ARG_TEARDOWN,
    ARG_DEVELOPER,
)


def _is_command_argument(arg: str) -> bool:
    assert arg
    return arg[0] != "-"


def _find_command_index(args: Iterable[str]) -> int:
    for index, arg in enumerate(args):
        if _is_command_argument(arg):
            return index
    raise IndexError("Not found command index.")


def get_global_namespace_and_command_args(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
    ignore_sys_argv=False,
) -> Tuple[Namespace, List[str]]:
    parser = ArgumentParser(
        usage="recc [global options] command [command options]",
        description="Restructured Engine for the Cyclops Cloud",
        epilog="Run 'recc command --help' for more information on a command",
        add_help=False,
    )

    for arg in GLOBAL_ARGS:
        parser.add_argument(*arg.keys, **arg.kwargs)

    if ignore_sys_argv:
        sys_argv = list()
    else:
        sys_argv = sys.argv[1:]

    args = cmdline if cmdline else sys_argv
    args = [str(a) for a in args if a is not None]
    try:
        command_args_index = 1 + _find_command_index(args)
    except IndexError:
        command_args_index = len(args)
    global_args = args[0:command_args_index]
    command_args = args[command_args_index:]

    if namespace:
        result = namespace
    else:
        result = Namespace()

    _, argv = parser.parse_known_args(global_args, result)
    result.help_message = parser.format_help()
    if argv:
        result.unrecognized_arguments = argv
    else:
        result.unrecognized_arguments = list()
    return result, command_args


def cast_global_config(obj: Any) -> GlobalConfig:
    return GlobalConfig(**vars(obj))


def get_global_config_and_command_args(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
) -> Tuple[GlobalConfig, List[str]]:
    obj, args = get_global_namespace_and_command_args(*cmdline, namespace)
    return cast_global_config(obj), args


def get_global_config_members() -> List[str]:
    return [key for key, val in get_type_hints(GlobalConfig).items()]
