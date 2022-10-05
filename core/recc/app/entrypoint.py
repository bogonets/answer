# -*- coding: utf-8 -*-

from typing import Callable, List, Optional

from recc.app.core_main import core_main
from recc.argparse.argument_parser import ArgumentMessage
from recc.argparse.command import Command
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.default_parser import get_command, parse_arguments_to_config
from recc.http.http_app import HttpAppCallback


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
        args = cmdline if cmdline else list()
        config = parse_arguments_to_config(*args)
    except ArgumentMessage as e:
        printer(e.message)
        return e.code
    except BaseException as e:
        printer(e)
        return 1

    cmd = get_command(config)
    assert cmd != Command.unknown

    if cmd == Command.core:
        assert isinstance(config, CoreConfig)
        return core_main(config, http_callback)
    elif cmd == Command.ctrl:
        raise NotImplementedError
    elif cmd == Command.task:
        raise NotImplementedError
    elif cmd == Command.daemon:
        raise NotImplementedError

    assert False, "Inaccessible section"


if __name__ == "__main__":
    exit(main())
