# -*- coding: utf-8 -*-

from typing import List

from recc import www as recc_www_module
from recc.argparse.argument import Argument
from recc.argparse.command import Command
from recc.argparse.config.global_config import GlobalConfig, create_usage
from recc.argparse.shortcut import Shortcut
from recc.package.package_utils import get_module_directory
from recc.variables.http import (
    DEFAULT_HTTP_BIND,
    DEFAULT_HTTP_PORT,
    DEFAULT_HTTP_TIMEOUT,
)
from recc.variables.plugin import CORE_PLUGIN_PREFIX, DAEMON_PLUGIN_PREFIX
from recc.variables.port import (
    DEFAULT_MANAGEABLE_MAXIMUM_PORT_NUMBER,
    DEFAULT_MANAGEABLE_MINIMUM_PORT_NUMBER,
)
from recc.variables.session import (
    SESSION_ACCESS_TOKEN_DURATION,
    SESSION_REFRESH_TOKEN_DURATION,
)

CORE_USAGE = create_usage(Command.core)
CORE_DESCRIPTION = "Core server"
CORE_EPILOG = ""
ENABLE_PUBLIC_SIGNUP = False

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
    help="Specifies the key used to sign the JWT token.",
)

ARG_CORE_PLUGIN_PREFIX = Argument(
    key="--core-plugin-prefix",
    last_injection_value=CORE_PLUGIN_PREFIX,
    cls=str,
    metavar="prefix",
    help="The prefix of the package name used to search for core plugins.",
)
ARG_CORE_PLUGIN_ALLOW = Argument(
    key="--core-plugin-allow",
    last_injection_value=list(),
    cls=List[str],
    delimiter=":",
    metavar="regex",
    action="append",
    help="Allow-list of found core plugins.",
)
ARG_CORE_PLUGIN_DENY = Argument(
    key="--core-plugin-deny",
    last_injection_value=list(),
    cls=List[str],
    delimiter=":",
    metavar="regex",
    action="append",
    help="Deny-list of found core plugins.",
)
ARG_DAEMON_PLUGIN_PREFIX = Argument(
    key="--daemon-plugin-prefix",
    last_injection_value=DAEMON_PLUGIN_PREFIX,
    cls=str,
    metavar="prefix",
    help="The prefix of the package name used to search for daemon plugins.",
)
ARG_DAEMON_PLUGIN_ALLOW = Argument(
    key="--daemon-plugin-allow",
    last_injection_value=list(),
    cls=List[str],
    delimiter=":",
    metavar="regex",
    action="append",
    help="Allow-list of found daemon plugins.",
)
ARG_DAEMON_PLUGIN_DENY = Argument(
    key="--daemon-plugin-deny",
    last_injection_value=list(),
    cls=List[str],
    delimiter=":",
    metavar="regex",
    action="append",
    help="Deny-list of found daemon plugins.",
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
    ARG_CORE_PLUGIN_PREFIX,
    ARG_CORE_PLUGIN_ALLOW,
    ARG_CORE_PLUGIN_DENY,
    ARG_DAEMON_PLUGIN_PREFIX,
    ARG_DAEMON_PLUGIN_ALLOW,
    ARG_DAEMON_PLUGIN_DENY,
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

    core_plugin_prefix: str
    core_plugin_allow: List[str]
    core_plugin_deny: List[str]
    daemon_plugin_prefix: str
    daemon_plugin_allow: List[str]
    daemon_plugin_deny: List[str]

    public_signup: bool
    access_token_duration: str
    refresh_token_duration: str
