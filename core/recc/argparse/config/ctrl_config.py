# -*- coding: utf-8 -*-

from recc.argparse.config.global_config import create_usage, GlobalConfig
from recc.argparse.argument import Argument
from recc.argparse.command import Command
from recc.variables.http import (
    DEFAULT_HTTP_ADDRESS,
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_SCHEME,
)

CTRL_USAGE = create_usage(Command.ctrl)
CTRL_DESCRIPTION = "Core client"
CTRL_EPILOG = ""

ARG_SCHEME = Argument(
    key="--scheme",
    last_injection_value=DEFAULT_SCHEME,
    cls=str,
    metavar="scheme",
    help="URI Scheme",
)
ARG_ADDRESS = Argument(
    key="--address",
    last_injection_value=DEFAULT_HTTP_ADDRESS,
    cls=str,
    metavar="bind",
    help="Binding address for HTTP server.",
)
ARG_TIMEOUT = Argument(
    key="--timeout",
    last_injection_value=DEFAULT_HTTP_TIMEOUT,
    cls=float,
    metavar="sec",
    help="HTTP module's timeout",
)

ARG_USERNAME = Argument(
    key="--username",
    last_injection_value="",
    cls=str,
    metavar="id",
    help="Username",
)
ARG_PASSWORD = Argument(
    key="--password",
    last_injection_value="",
    cls=str,
    metavar="pw",
    help="Password",
)

CTRL_ARGS = (
    ARG_SCHEME,
    ARG_ADDRESS,
    ARG_TIMEOUT,
    ARG_USERNAME,
    ARG_PASSWORD,
)


class CtrlConfig(GlobalConfig):
    scheme: str
    address: str
    timeout: float
    username: str
    password: str
