# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from typing import Optional, Any
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.argument import Shortcut, Argument
from recc.argparse.command import Command


class TaskConfig(GlobalConfig):

    task_address: str
    task_register: str
    task_workspace: str


ARG_HELP = Argument(
    key="--help",
    last_injection_value=False,
    shortcut=Shortcut.h,
    default=False,
    action="store_true",
    help=f"Print {Command.task.name} help message.",
)

ARG_ADDRESS = Argument(
    key="--task-address",
    last_injection_value="[::]",
    metavar="bind",
    help="RPC server bind address.",
)
ARG_REGISTER = Argument(
    key="--task-register",
    last_injection_value="",
    metavar="key",
    help="Register key.",  # RSA public key
)
ARG_WORKSPACE = Argument(
    key="--task-workspace",
    last_injection_value="",
    metavar="dir",
    help="Workspace directory.",
)

TASK_ARGS = (
    ARG_HELP,
    ARG_ADDRESS,
    ARG_REGISTER,
    ARG_WORKSPACE,
)


def get_task_namespace(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
) -> Namespace:
    parser = ArgumentParser(
        usage=f"recc {Command.task.name} [options]",
        description="Task runner",
        add_help=False,
    )

    for arg in TASK_ARGS:
        parser.add_argument(*arg.keys, **arg.kwargs)

    if namespace:
        result = namespace
    else:
        result = Namespace()

    args = [str(c) for c in cmdline if c is not None]
    _, argv = parser.parse_known_args(args, result)
    result.help_message = parser.format_help()
    result.unrecognized_arguments = argv
    return result


def cast_task_config(obj: Any) -> TaskConfig:
    return TaskConfig(**vars(obj))


def get_task_config(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
) -> TaskConfig:
    return cast_task_config(get_task_namespace(*cmdline, namespace))
