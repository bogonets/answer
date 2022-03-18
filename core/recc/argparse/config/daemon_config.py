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
    help="The address to bind the daemon service to.",
)
ARG_DAEMON_SCRIPT = Argument(
    key="--daemon-script",
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
ARG_DAEMON_VENV_DIR = Argument(
    key="--daemon-venv-dir",
    last_injection_value="",
    cls=str,
    metavar="dir",
    help="The daemon's venv directory.",
)

DAEMON_ARGS = (
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_SCRIPT,
    ARG_DAEMON_PACKAGES_DIR,
    ARG_DAEMON_VENV_DIR,
)


class DaemonConfig(GlobalConfig):

    daemon_address: str
    daemon_script: str
    daemon_packages_dir: List[str]
    daemon_venv_dir: str
