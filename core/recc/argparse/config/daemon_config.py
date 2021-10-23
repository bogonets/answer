# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Final, Optional, Any, List
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.argument import Shortcut, Argument
from recc.argparse.command import Command
from recc.argparse.config._utils import get_namespace, get_config_members


class DaemonConfig(GlobalConfig):

    daemon_address: str
    daemon_file: str


ARG_HELP = Argument(
    key="--help",
    last_injection_value=False,
    shortcut=Shortcut.h,
    default=False,
    action="store_true",
    help=f"Print {Command.daemon.name} help message.",
)

ARG_DAEMON_ADDRESS = Argument(
    key="--daemon-address",
    last_injection_value="",
    default=None,
    metavar="address",
    help="Daemon server bind address.",
)
ARG_DAEMON_FILE = Argument(
    key="--daemon-file",
    last_injection_value="",
    default=None,
    metavar="file",
    help="Daemon python file.",
)

DAEMON_USAGE: Final[str] = f"recc {Command.daemon.name} [options]"
DAEMON_DESCRIPTION: Final[str] = "Daemon runner"
DAEMON_ARGS = (
    ARG_HELP,
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_FILE,
)


def get_daemon_namespace(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
) -> Namespace:
    return get_namespace(
        *cmdline,
        usage=DAEMON_USAGE,
        description=DAEMON_DESCRIPTION,
        arguments=DAEMON_ARGS,
        namespace=namespace,
    )


def cast_daemon_config(obj: Any) -> DaemonConfig:
    return DaemonConfig(**vars(obj))


def get_daemon_config(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
) -> DaemonConfig:
    return cast_daemon_config(get_daemon_namespace(*cmdline, namespace))


def get_daemon_config_members(ignore_global_members=False) -> List[str]:
    return get_config_members(DaemonConfig, ignore_global_members)
