# -*- coding: utf-8 -*-

from typing import Optional, List, Callable
from recc.argparse.argument_parser import ArgumentMessage
from recc.argparse.default_parser import parse_arguments_to_config, get_command
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.config.ctrl_config import CtrlConfig
from recc.argparse.config.task_config import TaskConfig
from recc.argparse.config.daemon_config import DaemonConfig
from recc.argparse.command import Command
from recc.app.core_main import core_main
from recc.app.ctrl_main import ctrl_main
from recc.app.task_main import task_main
from recc.app.daemon_main import daemon_main
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
        assert isinstance(config, CtrlConfig)
        return ctrl_main(config)
    elif cmd == Command.task:
        assert isinstance(config, TaskConfig)
        return task_main(config)
    elif cmd == Command.daemon:
        assert isinstance(config, DaemonConfig)
        return daemon_main(config)

    assert False, "Inaccessible section"


if __name__ == "__main__":
    exit(main())
