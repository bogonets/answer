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
    daemon_packages_dir: str
    simply_logging: bool


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
ARG_DAEMON_PACKAGES_DIR = Argument(
    key="--daemon-packages-dir",
    last_injection_value="",
    default=None,
    metavar="dir",
    help="site-packages directory.",
)
ARG_SIMPLY_LOGGING = Argument(
    key="--simply-logging",
    last_injection_value=False,
    default=None,
    action="store_true",
    help="Simply logging.",
)


DAEMON_USAGE: Final[str] = f"recc {Command.daemon.name} [options]"
DAEMON_DESCRIPTION: Final[str] = "Daemon runner"
DAEMON_ARGS = (
    ARG_HELP,
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_FILE,
    ARG_DAEMON_PACKAGES_DIR,
    ARG_SIMPLY_LOGGING,
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
