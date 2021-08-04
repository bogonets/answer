# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Final, Optional, Any, List
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.argument import Shortcut, Argument
from recc.argparse.command import Command
from recc.argparse.config._utils import get_namespace, get_config_members
from recc.package.package_utils import get_module_directory
from recc import www as recc_www_module
from recc.variables.http import (
    DEFAULT_HTTP_BIND,
    DEFAULT_HTTP_PORT,
    DEFAULT_HTTP_TIMEOUT,
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
from recc.variables.port import (
    DEFAULT_MANAGEABLE_MINIMUM_PORT_NUMBER,
    DEFAULT_MANAGEABLE_MAXIMUM_PORT_NUMBER,
)
from recc.variables.user import ENABLE_PUBLIC_SIGNUP
from recc.variables.session import (
    SESSION_ACCESS_TOKEN_DURATION,
    SESSION_REFRESH_TOKEN_DURATION,
)


class CoreConfig(GlobalConfig):

    external_host: str

    http_bind: str
    http_port: int
    http_root: str
    http_timeout: float

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

    manage_port_min: int
    manage_port_max: int

    storage_root: str
    signature: str

    public_signup: bool
    access_token_duration: str
    refresh_token_duration: str


ARG_HELP = Argument(
    key="--help",
    last_injection_value=False,
    shortcut=Shortcut.h,
    default=False,
    action="store_true",
    help=f"Print {Command.core.name} help message.",
)

ARG_EXTERNAL_HOST = Argument(
    key="--external-host",
    last_injection_value="",
    metavar="host",
    help="External hostname",
)

ARG_HTTP_BIND = Argument(
    key="--http-bind",
    last_injection_value=DEFAULT_HTTP_BIND,
    shortcut=Shortcut.b,
    metavar="bind",
    help="Binding address for HTTP server.",
)
ARG_HTTP_PORT = Argument(
    key="--http-port",
    last_injection_value=DEFAULT_HTTP_PORT,
    shortcut=Shortcut.p,
    type=int,
    metavar="port",
    help="Binding port number for HTTP server.",
)
ARG_HTTP_ROOT = Argument(
    key="--http-root",
    last_injection_value=get_module_directory(recc_www_module),
    metavar="dir",
    help="Static file root directory for http server.",
)
ARG_HTTP_TIMEOUT = Argument(
    key="--http-timeout",
    last_injection_value=DEFAULT_HTTP_TIMEOUT,
    type=float,
    metavar="sec",
    help="HTTP module's timeout",
)

ARG_DATABASE_HOST = Argument(
    key="--database-host",
    last_injection_value="localhost",
    metavar="host",
    help="Database host address.",
)
ARG_DATABASE_PORT = Argument(
    key="--database-port",
    last_injection_value=5432,
    type=int,
    metavar="port",
    help="Database port number.",
)
ARG_DATABASE_USER = Argument(
    key="--database-user",
    last_injection_value="recc",
    metavar="id",
    help="Database user name.",
)
ARG_DATABASE_PW = Argument(
    key="--database-pw",
    last_injection_value="recc1234",
    metavar="pw",
    help="Database user's password.",
)
ARG_DATABASE_TYPE = Argument(
    key="--database-type",
    last_injection_value=DB_TYPE_NAME_POSTGRES,
    choices=(DB_TYPE_NAME_POSTGRES, DB_TYPE_NAME_MYSQL, DB_TYPE_NAME_SQLITE),
    help="Database type.",
)
ARG_DATABASE_NAME = Argument(
    key="--database-name",
    last_injection_value="recc",
    metavar="name",
    help="Database name.",
)

ARG_CACHE_HOST = Argument(
    key="--cache-host",
    last_injection_value="localhost",
    metavar="host",
    help="Cache server host.",
)
ARG_CACHE_PORT = Argument(
    key="--cache-port",
    last_injection_value=6379,
    type=int,
    metavar="port",
    help="Cache server port number.",
)
ARG_CACHE_PW = Argument(
    key="--cache-pw",
    last_injection_value="",
    metavar="pw",
    help="Cache server password.",
)
ARG_CACHE_TYPE = Argument(
    key="--cache-type",
    last_injection_value=CS_TYPE_NAME_REDIS,
    choices=(CS_TYPE_NAME_REDIS,),
    help="Cache server type.",
)

ARG_CONTAINER_HOST = Argument(
    key="--container-host",
    last_injection_value=DOCKER_SOCK_LOCAL_BASE_URL,
    metavar="host",
    help="Container manager host.",
)
ARG_CONTAINER_PORT = Argument(
    key="--container-port",
    last_injection_value=0,
    type=int,
    metavar="port",
    help="Container manager port number.",
)
ARG_CONTAINER_TYPE = Argument(
    key="--container-type",
    last_injection_value=CONTAINER_TYPE_DOCKER,
    choices=(CONTAINER_TYPE_DOCKER, CONTAINER_TYPE_SWARM, CONTAINER_TYPE_KUBERNETES),
    help="Container manager type.",
)
ARG_CONTAINER_ID = Argument(
    key="--container-id",
    last_injection_value="",
    help="The container ID when running inside the container.",
)

ARG_MANAGE_PORT_MIN = Argument(
    key="--manage-port-min",
    last_injection_value=DEFAULT_MANAGEABLE_MINIMUM_PORT_NUMBER,
    type=int,
    metavar="port",
    help="Manageable minimum port number.",
)
ARG_MANAGE_PORT_MAX = Argument(
    key="--manage-port-max",
    last_injection_value=DEFAULT_MANAGEABLE_MAXIMUM_PORT_NUMBER,
    type=int,
    metavar="port",
    help="Manageable maximum port number.",
)

ARG_STORAGE_ROOT = Argument(
    key="--storage-root",
    last_injection_value="",
    metavar="dir",
    help="Storage directory.",
)
ARG_SIGNATURE = Argument(
    key="--signature",
    last_injection_value="",
    shortcut=Shortcut.k,
    metavar="key",
    help="Specify the signing key.",
)

ARG_PUBLIC_SIGNUP = Argument(
    key="--public-signup",
    last_injection_value=ENABLE_PUBLIC_SIGNUP,
    action="store_true",
    help="Anyone can sign up.",
)
ARG_ACCESS_TOKEN_DURATION = Argument(
    key="--access-token-duration",
    last_injection_value=SESSION_ACCESS_TOKEN_DURATION,
    type=str,
    metavar="duration",
    help="Expiration period for the access token.",
)
ARG_REFRESH_TOKEN_DURATION = Argument(
    key="--refresh-token-duration",
    last_injection_value=SESSION_REFRESH_TOKEN_DURATION,
    type=str,
    metavar="duration",
    help="Expiration period for the refresh token.",
)

CORE_USAGE: Final[str] = f"recc {Command.core.name} [options]"
CORE_DESCRIPTION: Final[str] = "Core controller"
CORE_ARGS = (
    ARG_HELP,
    ARG_EXTERNAL_HOST,
    ARG_HTTP_BIND,
    ARG_HTTP_PORT,
    ARG_HTTP_ROOT,
    ARG_HTTP_TIMEOUT,
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
    ARG_MANAGE_PORT_MIN,
    ARG_MANAGE_PORT_MAX,
    ARG_STORAGE_ROOT,
    ARG_SIGNATURE,
    ARG_PUBLIC_SIGNUP,
    ARG_ACCESS_TOKEN_DURATION,
    ARG_REFRESH_TOKEN_DURATION,
)


def get_core_namespace(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
) -> Namespace:
    return get_namespace(
        *cmdline,
        usage=CORE_USAGE,
        description=CORE_DESCRIPTION,
        arguments=CORE_ARGS,
        namespace=namespace,
    )


def cast_core_config(obj: Any) -> CoreConfig:
    return CoreConfig(**vars(obj))


def get_core_config(*cmdline: Any, namespace: Optional[Namespace] = None) -> CoreConfig:
    return cast_core_config(get_core_namespace(*cmdline, namespace))


def get_core_config_members(ignore_global_members=False) -> List[str]:
    return get_config_members(CoreConfig, ignore_global_members)
