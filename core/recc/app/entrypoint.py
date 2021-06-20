# -*- coding: utf-8 -*-

from typing import Optional, List, Callable
from recc.argparse.default_parser import parse_arguments_to_config2, get_command
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.config.task_config import TaskConfig
from recc.argparse.command import Command
from recc.app.core_main import core_main
from recc.app.task_main import task_main
from recc.http.http_app import HttpAppCallback
from recc.util.version import version_text


def main(
    cmdline: Optional[List[str]] = None,
    *,
    http_callback: Optional[HttpAppCallback] = None,
    printer: Callable[..., None] = print,
) -> int:
    """
    The entry point for the core project.
    """

    try:
        config = parse_arguments_to_config2(cmdline)
    except BaseException as e:
        printer(e)
        return 1

    if config.unrecognized_arguments:
        printer(f"Unrecognized arguments: {config.unrecognized_arguments}")
        return 1

    if config.help:
        printer(config.help_message)
        return 0

    if config.version:  # nocov
        printer(version_text)
        return 0

    cmd = get_command(config)
    if cmd == Command.core:
        assert isinstance(config, CoreConfig)
        return core_main(config, http_callback)
    elif cmd == Command.task:
        assert isinstance(config, TaskConfig)
        return task_main(config)

    printer(f"Unknown command: {config.command}")
    return 1


if __name__ == "__main__":
    exit(main())
