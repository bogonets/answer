# -*- coding: utf-8 -*-

from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Dict, Tuple

from overrides import overrides

from recc.argparse.command import (
    COMMAND_ARGUMENT_KEY,
    HELP_ARGUMENT_KEY,
    SUBCOMMAND_HELP_ARGUMENT_KEY,
    VERSION_ARGUMENT_KEY,
    Command,
)
from recc.argparse.config.core_config import (
    CORE_ARGS,
    CORE_DESCRIPTION,
    CORE_EPILOG,
    CORE_USAGE,
)
from recc.argparse.config.global_config import (
    GLOBAL_ARGS,
    GLOBAL_DESCRIPTION,
    GLOBAL_EPILOG,
    GLOBAL_PROGRAM,
    GLOBAL_USAGE,
)

CmdToHelp = Dict[Command, str]
CmdToUsage = Dict[Command, str]


class ArgumentMessage(Exception):
    def __init__(self, message: str, code=2):
        super().__init__(message)
        self.message = message
        self.code = code


class _ArgumentParser(ArgumentParser):
    @overrides
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

    _add_subcommand_help(core_parser)

    helps = {
        Command.unknown: parser.format_help(),
        Command.core: core_parser.format_help(),
    }

    usages = {
        Command.unknown: parser.format_usage(),
        Command.core: core_parser.format_usage(),
    }

    return parser, helps, usages
