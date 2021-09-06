# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Final, Optional, Any, List
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.argument import Shortcut, Argument
from recc.argparse.command import Command
from recc.argparse.config._utils import get_namespace, get_config_members
from recc.variables.http import (
    DEFAULT_HTTP_ADDRESS,
    DEFAULT_HTTP_TIMEOUT,
)


class CtrlConfig(GlobalConfig):
    address: str
    timeout: float
    username: str
    password: str


ARG_HELP = Argument(
    key="--help",
    last_injection_value=False,
    shortcut=Shortcut.h,
    default=False,
    action="store_true",
    help=f"Print {Command.task.name} help message.",
)

ARG_ADDRESS = Argument(
    key="--address",
    last_injection_value=DEFAULT_HTTP_ADDRESS,
    metavar="bind",
    help="Binding address for HTTP server.",
)
ARG_TIMEOUT = Argument(
    key="--timeout",
    last_injection_value=DEFAULT_HTTP_TIMEOUT,
    type=float,
    metavar="sec",
    help="HTTP module's timeout",
)

ARG_USERNAME = Argument(
    key="--username",
    last_injection_value="",
    metavar="id",
    help="Username",
)
ARG_PASSWORD = Argument(
    key="--password",
    last_injection_value="",
    metavar="pw",
    help="Password",
)

CTRL_USAGE: Final[str] = f"recc {Command.ctrl.name} [options]"
CTRL_DESCRIPTION: Final[str] = "Command-line controller"
CTRL_ARGS = (
    ARG_HELP,
    ARG_ADDRESS,
    ARG_TIMEOUT,
    ARG_USERNAME,
    ARG_PASSWORD,
)


def get_ctrl_namespace(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
) -> Namespace:
    return get_namespace(
        *cmdline,
        usage=CTRL_USAGE,
        description=CTRL_DESCRIPTION,
        arguments=CTRL_ARGS,
        namespace=namespace,
    )


def cast_ctrl_config(obj: Any) -> CtrlConfig:
    return CtrlConfig(**vars(obj))


def get_ctrl_config(*cmdline: Any, namespace: Optional[Namespace] = None) -> CtrlConfig:
    return cast_ctrl_config(get_ctrl_namespace(*cmdline, namespace))


def get_ctrl_config_members(ignore_global_members=False) -> List[str]:
    return get_config_members(CtrlConfig, ignore_global_members)
