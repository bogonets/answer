# -*- coding: utf-8 -*-

import sys
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from typing import Iterable, Tuple, List, Optional, Any, get_type_hints
from recc.argparse.command import Command
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
from recc.variables.cache import CS_TYPE_NAME_REDIS
from recc.variables.container import (
    CONTAINER_TYPE_DOCKER,
    CONTAINER_TYPE_SWARM,
    CONTAINER_TYPE_KUBERNETES,
    DOCKER_SOCK_LOCAL_BASE_URL,
)
from recc.variables.database import (
    DB_TYPE_NAME_POSTGRES,
    DB_TYPE_NAME_MYSQL,
    DB_TYPE_NAME_SQLITE,
)
from recc.variables.storage import (
    STORAGE_SERVICE_TYPE_MINIO,
)

USAGE = "recc [global options] command [command options]"
DESCRIPTION = "Restructured Engine for the Cyclops Cloud"
EPILOG = f"""List of Commands:
  {Command.core.name}                  Core server
  {Command.task.name}                  Task process
  {Command.ctrl.name}                  Core client
  {Command.daemon.name}                Daemon process

Run 'recc command --help' for more information on a command
"""

LOOP_DRIVER_AIO = "aio"
LOOP_DRIVER_UV = "uv"

JSON_DRIVER_JSON = "json"
JSON_DRIVER_ORJSON = "orjson"

XML_DRIVER_XMLTODICT = "xmltodict"

YAML_DRIVER_PYYAML = "pyyaml"

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
    log_simply: bool

    loop_driver: str
    json_driver: str
    xml_driver: str
    yaml_driver: str

    database_host: str
    database_port: int
    database_user: str
    database_pw: str
    database_type: str
    database_name: str

    cache_host: str
    cache_port: int
    cache_pw: str
    cache_type: str

    container_host: str
    container_port: int
    container_type: str
    container_id: str
    container_image_validate: bool

    storage_type: str
    storage_host: str
    storage_port: int
    storage_user: str
    storage_pw: str
    storage_region: str
    storage_secure: bool

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
    default=None,
    metavar="file",
    help="Use the given config file.",
)
ARG_VERSION = Argument(
    key="--version",
    last_injection_value=False,
    default=False,  # It can only be set as a command line argument.
    action="store_true",
    help="Print the version number and exit.",
)
ARG_HELP = Argument(
    key="--help",
    last_injection_value=False,
    shortcut=Shortcut.h,
    default=False,  # It can only be set as a command line argument.
    action="store_true",
    help="Print help message.",
)

ARG_USER = Argument(
    key="--user",
    last_injection_value="recc",
    default=None,
    help="User name",
)
ARG_GROUP = Argument(
    key="--group",
    last_injection_value="recc",
    default=None,
    help="Group name",
)

ARG_LOG_CONFIG = Argument(
    key="--log-config",
    last_injection_value="logging.yml",
    default=None,
    metavar="file",
    help="Reads the logging configuration from a format file.",
)
ARG_LOG_LEVEL = Argument(
    key="--log-level",
    last_injection_value="",
    default=None,
    choices=LOG_LEVELS,
    help="Root logger severity. This value is set after configuring the log.",
)
ARG_LOG_SIMPLY = Argument(
    key="--log-simply",
    last_injection_value=False,
    default=None,
    action="store_true",
    help="Simply logging.",
)

ARG_LOOP_DRIVER = Argument(
    key="--loop-driver",
    last_injection_value=LOOP_DRIVER_AIO,
    default=None,
    choices=(LOOP_DRIVER_AIO, LOOP_DRIVER_UV),
    help="Async loop driver.",
)
ARG_JSON_DRIVER = Argument(
    key="--json-driver",
    last_injection_value=JSON_DRIVER_ORJSON,
    default=None,
    choices=(JSON_DRIVER_JSON, JSON_DRIVER_ORJSON),
    help="JSON encoder/decoder driver.",
)
ARG_XML_DRIVER = Argument(
    key="--xml-driver",
    last_injection_value=XML_DRIVER_XMLTODICT,
    default=None,
    choices=(XML_DRIVER_XMLTODICT,),
    help="XML encoder/decoder driver.",
)
ARG_YAML_DRIVER = Argument(
    key="--yaml-driver",
    last_injection_value=YAML_DRIVER_PYYAML,
    default=None,
    choices=(YAML_DRIVER_PYYAML,),
    help="YAML encoder/decoder driver.",
)

ARG_DATABASE_HOST = Argument(
    key="--database-host",
    last_injection_value="localhost",
    default=None,
    metavar="host",
    help="Database host address.",
)
ARG_DATABASE_PORT = Argument(
    key="--database-port",
    last_injection_value=5432,
    default=None,
    type=int,
    metavar="port",
    help="Database port number.",
)
ARG_DATABASE_USER = Argument(
    key="--database-user",
    last_injection_value="recc",
    default=None,
    metavar="id",
    help="Database user name.",
)
ARG_DATABASE_PW = Argument(
    key="--database-pw",
    last_injection_value="recc1234",
    default=None,
    metavar="pw",
    help="Database user's password.",
)
ARG_DATABASE_TYPE = Argument(
    key="--database-type",
    last_injection_value=DB_TYPE_NAME_POSTGRES,
    default=None,
    choices=(DB_TYPE_NAME_POSTGRES, DB_TYPE_NAME_MYSQL, DB_TYPE_NAME_SQLITE),
    help="Database type.",
)
ARG_DATABASE_NAME = Argument(
    key="--database-name",
    last_injection_value="recc",
    default=None,
    metavar="name",
    help="Database name.",
)

ARG_CACHE_HOST = Argument(
    key="--cache-host",
    last_injection_value="localhost",
    default=None,
    metavar="host",
    help="Cache server host.",
)
ARG_CACHE_PORT = Argument(
    key="--cache-port",
    last_injection_value=6379,
    default=None,
    type=int,
    metavar="port",
    help="Cache server port number.",
)
ARG_CACHE_PW = Argument(
    key="--cache-pw",
    last_injection_value="",
    default=None,
    metavar="pw",
    help="Cache server password.",
)
ARG_CACHE_TYPE = Argument(
    key="--cache-type",
    last_injection_value=CS_TYPE_NAME_REDIS,
    default=None,
    choices=(CS_TYPE_NAME_REDIS,),
    help="Cache server type.",
)

ARG_CONTAINER_HOST = Argument(
    key="--container-host",
    last_injection_value=DOCKER_SOCK_LOCAL_BASE_URL,
    default=None,
    metavar="host",
    help="Container manager host.",
)
ARG_CONTAINER_PORT = Argument(
    key="--container-port",
    last_injection_value=0,
    default=None,
    type=int,
    metavar="port",
    help="Container manager port number.",
)
ARG_CONTAINER_TYPE = Argument(
    key="--container-type",
    last_injection_value=CONTAINER_TYPE_DOCKER,
    default=None,
    choices=(CONTAINER_TYPE_DOCKER, CONTAINER_TYPE_SWARM, CONTAINER_TYPE_KUBERNETES),
    help="Container manager type.",
)
ARG_CONTAINER_ID = Argument(
    key="--container-id",
    last_injection_value="",
    default=None,
    metavar="id",
    help="The container ID when running inside the container.",
)
ARG_CONTAINER_IMAGE_VALIDATE = Argument(
    key="--container-image-validate",
    last_injection_value=False,
    default=None,
    action="store_true",
    help="Validate the container image.",
)

ARG_STORAGE_TYPE = Argument(
    key="--storage-type",
    last_injection_value=STORAGE_SERVICE_TYPE_MINIO,
    default=None,
    choices=(STORAGE_SERVICE_TYPE_MINIO,),
    help="Type of storage service.",
)
ARG_STORAGE_HOST = Argument(
    key="--storage-host",
    last_injection_value="localhost",
    default=None,
    metavar="host",
    help="Storage service host address.",
)
ARG_STORAGE_PORT = Argument(
    key="--storage-port",
    last_injection_value=9000,
    default=None,
    type=int,
    metavar="port",
    help="Storage service port number.",
)
ARG_STORAGE_USER = Argument(
    key="--storage-user",
    last_injection_value="recc",
    default=None,
    metavar="id",
    help="Storage service user name. (or access key)",
)
ARG_STORAGE_PW = Argument(
    key="--storage-pw",
    last_injection_value="recc1234",
    default=None,
    metavar="pw",
    help="Storage service user's password. (or secret key)",
)
ARG_STORAGE_SECURE = Argument(
    key="--storage-secure",
    last_injection_value=False,
    default=None,
    action="store_true",
    help="Storage service secure flag.",
)
ARG_STORAGE_REGION = Argument(
    key="--storage-region",
    last_injection_value="",
    default=None,
    metavar="region",
    help="Storage service region.",
)

ARG_SUPPRESS_PRINT = Argument(
    key="--suppress-print",
    last_injection_value=False,
    default=None,
    action="store_true",
    help="Suppress printing.",
)
ARG_VERBOSE = Argument(
    key="--verbose",
    last_injection_value=0,
    shortcut=Shortcut.v,
    default=None,
    action="count",
    help="Be more verbose/talkative during the operation.",
)
ARG_TEARDOWN = Argument(
    key="--teardown",
    last_injection_value=False,
    default=None,
    action="store_true",
    help="When the server is shut down, all resources created are released.",
)
ARG_DEVELOPER = Argument(
    key="--developer",
    last_injection_value=False,
    shortcut=Shortcut.d,
    default=None,
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
    ARG_LOG_SIMPLY,
    ARG_LOOP_DRIVER,
    ARG_JSON_DRIVER,
    ARG_XML_DRIVER,
    ARG_YAML_DRIVER,
    ARG_DATABASE_HOST,
    ARG_DATABASE_PORT,
    ARG_DATABASE_USER,
    ARG_DATABASE_PW,
    ARG_DATABASE_TYPE,
    ARG_DATABASE_NAME,
    ARG_CACHE_HOST,
    ARG_CACHE_PORT,
    ARG_CACHE_PW,
    ARG_CACHE_TYPE,
    ARG_CONTAINER_HOST,
    ARG_CONTAINER_PORT,
    ARG_CONTAINER_TYPE,
    ARG_CONTAINER_ID,
    ARG_CONTAINER_IMAGE_VALIDATE,
    ARG_STORAGE_TYPE,
    ARG_STORAGE_HOST,
    ARG_STORAGE_PORT,
    ARG_STORAGE_USER,
    ARG_STORAGE_PW,
    ARG_STORAGE_REGION,
    ARG_STORAGE_SECURE,
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
        usage=USAGE,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawTextHelpFormatter,
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
