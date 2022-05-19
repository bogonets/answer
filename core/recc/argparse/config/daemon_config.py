# -*- coding: utf-8 -*-

from typing import List

from recc.argparse.argument import Argument
from recc.argparse.command import Command
from recc.argparse.config.global_config import GlobalConfig, create_usage

DAEMON_USAGE = create_usage(Command.daemon)
DAEMON_DESCRIPTION = "Daemon process"
DAEMON_EPILOG = ""

ARG_DAEMON_ADDRESS = Argument(
    key="--daemon-address",
    last_injection_value="",
    cls=str,
    metavar="address",
    help="The address to bind the daemon service to.",
)
ARG_DAEMON_MODULE = Argument(
    key="--daemon-module",
    last_injection_value="",
    cls=str,
    metavar="file",
    help="A Python script with an entry point for the daemon.",
)
ARG_DAEMON_PACKAGES_DIR = Argument(
    key="--daemon-packages-dir",
    last_injection_value=list(),
    cls=List[str],
    delimiter=":",
    metavar="dir",
    action="append",
    help="Additional packages directory.",
)

DAEMON_ARGS = (
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_MODULE,
    ARG_DAEMON_PACKAGES_DIR,
)


class DaemonConfig(GlobalConfig):

    daemon_address: str
    daemon_module: str
    daemon_packages_dir: List[str]
