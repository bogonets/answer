# -*- coding: utf-8 -*-

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from functools import lru_cache
from typing import Final

from recc.logging.logging import SEVERITIES

PROG: Final[str] = "recc"
DESCRIPTION: Final[str] = "Restructured Engine for the Cyclops Cloud (ANSWER)"
EPILOG: Final[str] = ""


@lru_cache
def version() -> str:
    # [IMPORTANT] Avoid 'circular import' issues
    from mime_parser import __version__

    return __version__


def add_config_file_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--config",
        "-c",
        metavar="file",
        help="Use the given config file",
    )
    return parser


def add_http_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--http-bind",
        "-b",
        metavar="bind",
        help="Binding address for HTTP server",
    )
    parser.add_argument(
        "--http-port",
        "-p",
        type=int,
        metavar="port",
        help="Binding port number for HTTP server",
    )
    parser.add_argument(
        "--http-root",
        metavar="dir",
        help="Static file root directory for http server",
    )
    parser.add_argument(
        "--http-timeout",
        type=float,
        metavar="sec",
        help="HTTP module's timeout",
    )
    return parser


def add_database_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--database-host",
        metavar="host",
        help="Database host address",
    )
    parser.add_argument(
        "--database-port",
        type=int,
        metavar="port",
        help="Database port number",
    )
    parser.add_argument(
        "--database-user",
        metavar="id",
        help="Database user name",
    )
    parser.add_argument(
        "--database-pw",
        metavar="pw",
        help="Database user's password",
    )
    parser.add_argument(
        "--database-name",
        metavar="name",
        help="Database name",
    )
    parser.add_argument(
        "--database-timeout",
        type=float,
        metavar="sec",
        help="Database command timeout",
    )
    return parser


def add_cache_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--cache-host",
        metavar="host",
        help="Cache server host",
    )
    parser.add_argument(
        "--cache-port",
        type=int,
        metavar="port",
        help="Cache server port number",
    )
    parser.add_argument(
        "--cache-secret",
        metavar="secret",
        help="Cache server secret",
    )
    parser.add_argument(
        "--cache-prefix",
        metavar="prefix",
        help="Cache key prefix",
    )
    parser.add_argument(
        "--cache-timeout",
        type=float,
        metavar="sec",
        help="Cache command timeout",
    )
    return parser


def add_storage_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--storage-host",
        metavar="host",
        help="Storage service host address",
    )
    parser.add_argument(
        "--storage-port",
        type=int,
        metavar="port",
        help="Storage service port number",
    )
    parser.add_argument(
        "--storage-access",
        metavar="id",
        help="Storage access key",
    )
    parser.add_argument(
        "--storage-secret",
        metavar="pw",
        help="Storage secret key",
    )
    parser.add_argument(
        "--storage-region",
        metavar="region",
        help="Storage service region",
    )
    parser.add_argument(
        "--storage-bucket",
        metavar="bucket",
        help="Storage service bucket",
    )
    parser.add_argument(
        "--storage-prefix",
        metavar="path",
        help="Storage service prefix",
    )
    parser.add_argument(
        "--storage-secure",
        default=None,
        action="store_true",
        help="Enable storage service secure flag",
    )
    parser.add_argument(
        "--storage-timeout",
        type=float,
        metavar="sec",
        help="Storage request timeout",
    )
    return parser


def add_plugin_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--plugin-prefix",
        metavar="prefix",
        help="The prefix of the package name used to search for core plugins",
    )
    parser.add_argument(
        "--plugin-allow",
        action="append",
        metavar="regex",
        help="Allow-list of found core plugins",
    )
    parser.add_argument(
        "--plugin-deny",
        action="append",
        metavar="regex",
        help="Deny-list of found core plugins",
    )
    return parser


def add_logging_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--log-config",
        metavar="file",
        help="Reads the logging configuration from a format file",
    )
    parser.add_argument(
        "--log-level",
        choices=SEVERITIES,
        help="Logging severity",
    )
    parser.add_argument(
        "--log-simply",
        default=None,
        action="store_true",
        help="Use simple logging",
    )
    return parser


def add_token_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--signature",
        "-k",
        metavar="key",
        help="Specifies the key used to sign the JWT token",
    )
    parser.add_argument(
        "--access-token-duration",
        metavar="duration",
        help="Expiration period for the access token",
    )
    parser.add_argument(
        "--refresh-token-duration",
        metavar="duration",
        help="Expiration period for the refresh token",
    )
    return parser


def default_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=PROG,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )

    add_config_file_arguments(parser)
    add_http_arguments(parser)
    add_database_arguments(parser)
    add_cache_arguments(parser)
    add_storage_arguments(parser)
    add_plugin_arguments(parser)
    add_logging_arguments(parser)
    add_token_arguments(parser)

    parser.add_argument(
        "--public-signup",
        default=None,
        action="store_true",
        help="Anyone can sign up",
    )
    parser.add_argument(
        "--install-uvloop",
        default=None,
        action="store_true",
        help="Install the event loop policy as uvloop",
    )
    parser.add_argument(
        "--teardown",
        default=None,
        action="store_true",
        help="When the server is shut down, all resources created are released",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        help="Be more verbose/talkative during the operation",
    )
    parser.add_argument(
        "--developer",
        "-d",
        default=None,
        action="store_true",
        help="Enable developer mode",
    )

    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=version(),
    )

    return parser
