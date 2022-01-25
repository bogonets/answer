# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Final, Union
from recc.argparse.command import Command
from recc.argparse.argument import Argument
from recc.argparse.shortcut import Shortcut
from recc.logging.logging import (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)
from recc.variables.cache import CS_TYPE_NAME_REDIS, CACHE_PREFIX_ROOT
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
    DATABASE_COMMAND_TIMEOUT_SECONDS,
)
from recc.variables.storage import (
    STORAGE_SERVICE_TYPE_MINIO,
    STORAGE_REQUEST_TIMEOUT,
)

_DEFAULT_PROGRAM: Final[str] = "recc"
_DEFAULT_SUBCOMMAND: Final[str] = "{subcommand}"


def create_usage(
    subcommand: Union[Command, str],
    program=_DEFAULT_PROGRAM,
) -> str:
    if isinstance(subcommand, Command):
        sub = subcommand.name
    else:
        assert isinstance(subcommand, str)
        sub = subcommand

    return "{program} [global options] {subcommand} [subcommand options]".format(
        program=program, subcommand=sub
    )


GLOBAL_PROGRAM: Final[str] = _DEFAULT_PROGRAM
GLOBAL_USAGE = create_usage(_DEFAULT_SUBCOMMAND)
GLOBAL_DESCRIPTION = "Restructured Engine for the Cyclops Cloud"
GLOBAL_EPILOG = f"""List of Subcommands:
  {Command.core.name}                  Core server
  {Command.ctrl.name}                  Core client
  {Command.task.name}                  Task process
  {Command.daemon.name}                Daemon process

Run '{GLOBAL_PROGRAM} subcommand --help' for more information on a command
"""

LOOP_DRIVER_AIO = "aio"
LOOP_DRIVER_UV = "uv"
LOOP_DRIVERS = (LOOP_DRIVER_AIO, LOOP_DRIVER_UV)

JSON_DRIVER_JSON = "json"
JSON_DRIVER_ORJSON = "orjson"
JSON_DRIVERS = (JSON_DRIVER_JSON, JSON_DRIVER_ORJSON)

XML_DRIVER_XMLTODICT = "xmltodict"
XML_DRIVERS = (XML_DRIVER_XMLTODICT,)

YAML_DRIVER_PYYAML = "pyyaml"
YAML_DRIVERS = (YAML_DRIVER_PYYAML,)

LOG_LEVELS = (
    SEVERITY_NAME_CRITICAL,
    SEVERITY_NAME_ERROR,
    SEVERITY_NAME_WARNING,
    SEVERITY_NAME_INFO,
    SEVERITY_NAME_DEBUG,
    SEVERITY_NAME_NOTSET,
    SEVERITY_NAME_OFF,
)

ARG_CONFIG = Argument(
    key="--config",
    last_injection_value="",
    cls=str,
    shortcut=Shortcut.c,
    metavar="file",
    help="Use the given config file.",
)
ARG_USER = Argument(
    key="--user",
    last_injection_value="recc",
    cls=str,
    help="User name",
)
ARG_GROUP = Argument(
    key="--group",
    last_injection_value="recc",
    cls=str,
    help="Group name",
)

ARG_LOG_CONFIG = Argument(
    key="--log-config",
    last_injection_value="logging.yml",
    cls=str,
    metavar="file",
    help="Reads the logging configuration from a format file.",
)
ARG_LOG_LEVEL = Argument(
    key="--log-level",
    last_injection_value="",
    cls=str,
    choices=LOG_LEVELS,
    help="Root logger severity. This value is set after configuring the log.",
)
ARG_LOG_SIMPLY = Argument(
    key="--log-simply",
    last_injection_value=False,
    cls=bool,
    action="store_true",
    help="Simply logging.",
)

ARG_LOOP_DRIVER = Argument(
    key="--loop-driver",
    last_injection_value=LOOP_DRIVER_AIO,
    cls=str,
    choices=LOOP_DRIVERS,
    help="Async loop driver.",
)
ARG_JSON_DRIVER = Argument(
    key="--json-driver",
    last_injection_value=JSON_DRIVER_ORJSON,
    cls=str,
    choices=JSON_DRIVERS,
    help="JSON encoder/decoder driver.",
)
ARG_XML_DRIVER = Argument(
    key="--xml-driver",
    last_injection_value=XML_DRIVER_XMLTODICT,
    cls=str,
    choices=(XML_DRIVER_XMLTODICT,),
    help="XML encoder/decoder driver.",
)
ARG_YAML_DRIVER = Argument(
    key="--yaml-driver",
    last_injection_value=YAML_DRIVER_PYYAML,
    cls=str,
    choices=YAML_DRIVERS,
    help="YAML encoder/decoder driver.",
)

ARG_DATABASE_HOST = Argument(
    key="--database-host",
    last_injection_value="localhost",
    cls=str,
    metavar="host",
    help="Database host address.",
)
ARG_DATABASE_PORT = Argument(
    key="--database-port",
    last_injection_value=5432,
    cls=int,
    metavar="port",
    help="Database port number.",
)
ARG_DATABASE_USER = Argument(
    key="--database-user",
    last_injection_value="recc",
    cls=str,
    metavar="id",
    help="Database user name.",
)
ARG_DATABASE_PW = Argument(
    key="--database-pw",
    last_injection_value="recc1234",
    cls=str,
    metavar="pw",
    help="Database user's password.",
)
ARG_DATABASE_TYPE = Argument(
    key="--database-type",
    last_injection_value=DB_TYPE_NAME_POSTGRES,
    cls=str,
    choices=(DB_TYPE_NAME_POSTGRES, DB_TYPE_NAME_MYSQL, DB_TYPE_NAME_SQLITE),
    help="Database type.",
)
ARG_DATABASE_NAME = Argument(
    key="--database-name",
    last_injection_value="recc",
    cls=str,
    metavar="name",
    help="Database name.",
)
ARG_DATABASE_TIMEOUT = Argument(
    key="--database-timeout",
    last_injection_value=DATABASE_COMMAND_TIMEOUT_SECONDS,
    cls=float,
    metavar="sec",
    help="Database command timeout.",
)

ARG_CACHE_HOST = Argument(
    key="--cache-host",
    last_injection_value="localhost",
    cls=str,
    metavar="host",
    help="Cache server host.",
)
ARG_CACHE_PORT = Argument(
    key="--cache-port",
    last_injection_value=6379,
    cls=int,
    metavar="port",
    help="Cache server port number.",
)
ARG_CACHE_PW = Argument(
    key="--cache-pw",
    last_injection_value="",
    cls=str,
    metavar="pw",
    help="Cache server password.",
)
ARG_CACHE_TYPE = Argument(
    key="--cache-type",
    last_injection_value=CS_TYPE_NAME_REDIS,
    cls=str,
    choices=(CS_TYPE_NAME_REDIS,),
    help="Cache server type.",
)
ARG_CACHE_PREFIX = Argument(
    key="--cache-prefix",
    last_injection_value=CACHE_PREFIX_ROOT,
    cls=str,
    help="Cache key prefix.",
)

ARG_CONTAINER_HOST = Argument(
    key="--container-host",
    last_injection_value=DOCKER_SOCK_LOCAL_BASE_URL,
    cls=str,
    metavar="host",
    help="Container manager host.",
)
ARG_CONTAINER_PORT = Argument(
    key="--container-port",
    last_injection_value=0,
    cls=int,
    metavar="port",
    help="Container manager port number.",
)
ARG_CONTAINER_TYPE = Argument(
    key="--container-type",
    last_injection_value=CONTAINER_TYPE_DOCKER,
    cls=str,
    choices=(CONTAINER_TYPE_DOCKER, CONTAINER_TYPE_SWARM, CONTAINER_TYPE_KUBERNETES),
    help="Container manager type.",
)
ARG_CONTAINER_ID = Argument(
    key="--container-id",
    last_injection_value="",
    cls=str,
    metavar="id",
    help="The container ID when running inside the container.",
)
ARG_CONTAINER_IMAGE_VALIDATE = Argument(
    key="--container-image-validate",
    last_injection_value=False,
    cls=bool,
    action="store_true",
    help="Validate the container image.",
)

ARG_STORAGE_TYPE = Argument(
    key="--storage-type",
    last_injection_value=STORAGE_SERVICE_TYPE_MINIO,
    cls=str,
    choices=(STORAGE_SERVICE_TYPE_MINIO,),
    help="Type of storage service.",
)
ARG_STORAGE_HOST = Argument(
    key="--storage-host",
    last_injection_value="localhost",
    cls=str,
    metavar="host",
    help="Storage service host address.",
)
ARG_STORAGE_PORT = Argument(
    key="--storage-port",
    last_injection_value=9000,
    cls=int,
    metavar="port",
    help="Storage service port number.",
)
ARG_STORAGE_USER = Argument(
    key="--storage-user",
    last_injection_value="recc",
    cls=str,
    metavar="id",
    help="Storage service user name. (or access key)",
)
ARG_STORAGE_PW = Argument(
    key="--storage-pw",
    last_injection_value="recc1234",
    cls=str,
    metavar="pw",
    help="Storage service user's password. (or secret key)",
)
ARG_STORAGE_REGION = Argument(
    key="--storage-region",
    last_injection_value="",
    cls=str,
    metavar="region",
    help="Storage service region.",
)
ARG_STORAGE_SECURE = Argument(
    key="--storage-secure",
    last_injection_value=False,
    cls=bool,
    action="store_true",
    help="Storage service secure flag.",
)
ARG_STORAGE_TIMEOUT = Argument(
    key="--storage-timeout",
    last_injection_value=STORAGE_REQUEST_TIMEOUT,
    cls=float,
    metavar="sec",
    help="Storage request timeout.",
)


ARG_SUPPRESS_PRINT = Argument(
    key="--suppress-print",
    last_injection_value=False,
    cls=bool,
    action="store_true",
    help="Suppress printing.",
)
ARG_VERBOSE = Argument(
    key="--verbose",
    last_injection_value=0,
    cls=int,
    shortcut=Shortcut.v,
    action="count",
    help="Be more verbose/talkative during the operation.",
)
ARG_TEARDOWN = Argument(
    key="--teardown",
    last_injection_value=False,
    cls=bool,
    action="store_true",
    help="When the server is shut down, all resources created are released.",
)
ARG_DEVELOPER = Argument(
    key="--developer",
    last_injection_value=False,
    cls=bool,
    shortcut=Shortcut.d,
    action="store_true",
    help="Developer mode.",
)

GLOBAL_ARGS = (
    ARG_CONFIG,
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
    ARG_DATABASE_TIMEOUT,
    ARG_CACHE_HOST,
    ARG_CACHE_PORT,
    ARG_CACHE_PW,
    ARG_CACHE_TYPE,
    ARG_CACHE_PREFIX,
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
    ARG_STORAGE_TIMEOUT,
    ARG_SUPPRESS_PRINT,
    ARG_VERBOSE,
    ARG_TEARDOWN,
    ARG_DEVELOPER,
)


class GlobalConfig(Namespace):

    command: str

    config: str
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
    database_timeout: float

    cache_host: str
    cache_port: int
    cache_pw: str
    cache_type: str
    cache_prefix: str

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
    storage_timeout: float

    suppress_print: bool
    verbose: int
    teardown: bool
    developer: bool
