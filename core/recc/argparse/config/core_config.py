# -*- coding: utf-8 -*-

from recc.argparse.config.global_config import create_usage, GlobalConfig
from recc.argparse.argument import Argument
from recc.argparse.shortcut import Shortcut
from recc.argparse.command import Command
from recc.package.package_utils import get_module_directory
from recc import www as recc_www_module
from recc.variables.http import (
    DEFAULT_HTTP_BIND,
    DEFAULT_HTTP_PORT,
    DEFAULT_HTTP_TIMEOUT,
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

CORE_USAGE = create_usage(Command.core)
CORE_DESCRIPTION = "Core server"
CORE_EPILOG = ""

ARG_EXTERNAL_HOST = Argument(
    key="--external-host",
    last_injection_value="",
    cls=str,
    metavar="host",
    help="External hostname",
)

ARG_HTTP_BIND = Argument(
    key="--http-bind",
    last_injection_value=DEFAULT_HTTP_BIND,
    cls=str,
    shortcut=Shortcut.b,
    metavar="bind",
    help="Binding address for HTTP server.",
)
ARG_HTTP_PORT = Argument(
    key="--http-port",
    last_injection_value=DEFAULT_HTTP_PORT,
    cls=int,
    shortcut=Shortcut.p,
    metavar="port",
    help="Binding port number for HTTP server.",
)
ARG_HTTP_ROOT = Argument(
    key="--http-root",
    last_injection_value=get_module_directory(recc_www_module),
    cls=str,
    metavar="dir",
    help="Static file root directory for http server.",
)
ARG_HTTP_TIMEOUT = Argument(
    key="--http-timeout",
    last_injection_value=DEFAULT_HTTP_TIMEOUT,
    cls=float,
    metavar="sec",
    help="HTTP module's timeout",
)

ARG_MANAGE_PORT_MIN = Argument(
    key="--manage-port-min",
    last_injection_value=DEFAULT_MANAGEABLE_MINIMUM_PORT_NUMBER,
    cls=int,
    metavar="port",
    help="Manageable minimum port number.",
)
ARG_MANAGE_PORT_MAX = Argument(
    key="--manage-port-max",
    last_injection_value=DEFAULT_MANAGEABLE_MAXIMUM_PORT_NUMBER,
    cls=int,
    metavar="port",
    help="Manageable maximum port number.",
)

ARG_LOCAL_STORAGE = Argument(
    key="--local-storage",
    last_injection_value="",
    cls=str,
    metavar="dir",
    help="The root directory of local storage.",
)

ARG_SIGNATURE = Argument(
    key="--signature",
    last_injection_value="",
    cls=str,
    shortcut=Shortcut.k,
    metavar="key",
    help="Specify the signing key.",
)

ARG_PUBLIC_SIGNUP = Argument(
    key="--public-signup",
    last_injection_value=ENABLE_PUBLIC_SIGNUP,
    cls=bool,
    action="store_true",
    help="Anyone can sign up.",
)
ARG_ACCESS_TOKEN_DURATION = Argument(
    key="--access-token-duration",
    last_injection_value=SESSION_ACCESS_TOKEN_DURATION,
    cls=str,
    metavar="duration",
    help="Expiration period for the access token.",
)
ARG_REFRESH_TOKEN_DURATION = Argument(
    key="--refresh-token-duration",
    last_injection_value=SESSION_REFRESH_TOKEN_DURATION,
    cls=str,
    metavar="duration",
    help="Expiration period for the refresh token.",
)

CORE_ARGS = (
    ARG_EXTERNAL_HOST,
    ARG_HTTP_BIND,
    ARG_HTTP_PORT,
    ARG_HTTP_ROOT,
    ARG_HTTP_TIMEOUT,
    ARG_MANAGE_PORT_MIN,
    ARG_MANAGE_PORT_MAX,
    ARG_LOCAL_STORAGE,
    ARG_SIGNATURE,
    ARG_PUBLIC_SIGNUP,
    ARG_ACCESS_TOKEN_DURATION,
    ARG_REFRESH_TOKEN_DURATION,
)


class CoreConfig(GlobalConfig):

    external_host: str

    http_bind: str
    http_port: int
    http_root: str
    http_timeout: float

    manage_port_min: int
    manage_port_max: int

    local_storage: str

    signature: str

    public_signup: bool
    access_token_duration: str
    refresh_token_duration: str
