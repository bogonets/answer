# -*- coding: utf-8 -*-

from typing import List
from recc.argparse.config.global_config import create_usage, GlobalConfig
from recc.argparse.argument import Argument
from recc.argparse.command import Command

DAEMON_USAGE = create_usage(Command.daemon)
DAEMON_DESCRIPTION = "Daemon process"
DAEMON_EPILOG = ""

ARG_DAEMON_ADDRESS = Argument(
    key="--daemon-address",
    last_injection_value="",
    cls=str,
    metavar="address",
    help="Daemon server bind address.",
)
ARG_DAEMON_SCRIPT = Argument(
    key="--daemon-script",
    last_injection_value="",
    cls=str,
    metavar="file",
    help="Daemon python file.",
)
ARG_DAEMON_PACKAGES_DIR = Argument(
    key="--daemon-packages-dir",
    last_injection_value=list(),
    cls=List[str],
    delimiter=":",
    metavar="dir",
    action="append",
    help="Original site-packages directory.",
)

DAEMON_ARGS = (
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_SCRIPT,
    ARG_DAEMON_PACKAGES_DIR,
)


class DaemonConfig(GlobalConfig):

    daemon_address: str
    daemon_script: str
    daemon_packages_dir: List[str]
