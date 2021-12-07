# -*- coding: utf-8 -*-

from typing import Tuple, Dict
from argparse import ArgumentParser, RawTextHelpFormatter
from recc.argparse.command import (
    COMMAND_ARGUMENT_KEY,
    HELP_ARGUMENT_KEY,
    SUBCOMMAND_HELP_ARGUMENT_KEY,
    VERSION_ARGUMENT_KEY,
    Command,
)
from recc.argparse.config.global_config import (
    GLOBAL_ARGS,
    GLOBAL_PROGRAM,
    GLOBAL_USAGE,
    GLOBAL_DESCRIPTION,
    GLOBAL_EPILOG,
)
from recc.argparse.config.core_config import (
    CORE_USAGE,
    CORE_DESCRIPTION,
    CORE_EPILOG,
    CORE_ARGS,
)
from recc.argparse.config.ctrl_config import (
    CTRL_USAGE,
    CTRL_DESCRIPTION,
    CTRL_EPILOG,
    CTRL_ARGS,
)
from recc.argparse.config.daemon_config import (
    DAEMON_USAGE,
    DAEMON_DESCRIPTION,
    DAEMON_EPILOG,
    DAEMON_ARGS,
)
from recc.argparse.config.task_config import (
    TASK_USAGE,
    TASK_DESCRIPTION,
    TASK_EPILOG,
    TASK_ARGS,
)

CmdToHelp = Dict[Command, str]
CmdToUsage = Dict[Command, str]


class ArgumentMessage(Exception):
    def __init__(self, message: str, code=2):
        super().__init__(message)
        self.message = message
        self.code = code


class _ArgumentParser(ArgumentParser):
    def error(self, message):
        raise ArgumentMessage(message)


def _add_help(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--help",
        "-h",
        action="store_true",
        dest=HELP_ARGUMENT_KEY,
        help="Print this help message and exit",
    )


def _add_subcommand_help(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--help",
        "-h",
        action="store_true",
        dest=SUBCOMMAND_HELP_ARGUMENT_KEY,
        help="Print this help message and exit",
    )


def _add_version(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--version",
        action="store_true",
        dest=VERSION_ARGUMENT_KEY,
        help="Print the version number and exit",
    )


def create_argument_parser() -> Tuple[ArgumentParser, CmdToHelp, CmdToUsage]:
    parser = _ArgumentParser(
        prog=GLOBAL_PROGRAM,
        usage=GLOBAL_USAGE,
        description=GLOBAL_DESCRIPTION,
        epilog=GLOBAL_EPILOG,
        formatter_class=RawTextHelpFormatter,
        add_help=False,
        allow_abbrev=False,
    )
    for arg in GLOBAL_ARGS:
        parser.add_argument(*arg.keys, **arg.kwargs)

    _add_help(parser)
    _add_version(parser)

    subparsers = parser.add_subparsers(
        title="Subcommands",
        dest=COMMAND_ARGUMENT_KEY,
    )

    core_parser = subparsers.add_parser(
        name=Command.core.name,
        usage=CORE_USAGE,
        description=CORE_DESCRIPTION,
        epilog=CORE_EPILOG,
        add_help=False,
    )
    for arg in CORE_ARGS:
        core_parser.add_argument(*arg.keys, **arg.kwargs)

    task_parser = subparsers.add_parser(
        name=Command.task.name,
        usage=TASK_USAGE,
        description=TASK_DESCRIPTION,
        epilog=TASK_EPILOG,
        add_help=False,
    )
    for arg in TASK_ARGS:
        task_parser.add_argument(*arg.keys, **arg.kwargs)

    ctrl_parser = subparsers.add_parser(
        name=Command.ctrl.name,
        usage=CTRL_USAGE,
        description=CTRL_DESCRIPTION,
        epilog=CTRL_EPILOG,
        add_help=False,
    )
    for arg in CTRL_ARGS:
        ctrl_parser.add_argument(*arg.keys, **arg.kwargs)

    daemon_parser = subparsers.add_parser(
        name=Command.daemon.name,
        usage=DAEMON_USAGE,
        description=DAEMON_DESCRIPTION,
        epilog=DAEMON_EPILOG,
        add_help=False,
    )
    for arg in DAEMON_ARGS:
        daemon_parser.add_argument(*arg.keys, **arg.kwargs)

    _add_subcommand_help(core_parser)
    _add_subcommand_help(task_parser)
    _add_subcommand_help(ctrl_parser)
    _add_subcommand_help(daemon_parser)

    helps = {
        Command.unknown: parser.format_help(),
        Command.core: core_parser.format_help(),
        Command.task: task_parser.format_help(),
        Command.ctrl: ctrl_parser.format_help(),
        Command.daemon: daemon_parser.format_help(),
    }

    usages = {
        Command.unknown: parser.format_usage(),
        Command.core: core_parser.format_usage(),
        Command.task: task_parser.format_usage(),
        Command.ctrl: ctrl_parser.format_usage(),
        Command.daemon: daemon_parser.format_usage(),
    }

    return parser, helps, usages
