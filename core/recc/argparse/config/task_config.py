# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from typing import Optional, Any, List, get_type_hints
from recc.argparse.config.global_config import GlobalConfig, get_global_config_members
from recc.argparse.argument import Shortcut, Argument
from recc.argparse.command import Command


class TaskConfig(GlobalConfig):

    task_address: str
    task_register: str

    task_group: str
    task_project: str
    task_name: str

    task_workspace_dir: str
    task_package_dir: str
    task_cache_dir: str


ARG_HELP = Argument(
    key="--help",
    last_injection_value=False,
    shortcut=Shortcut.h,
    default=False,
    action="store_true",
    help=f"Print {Command.task.name} help message.",
)

ARG_TASK_ADDRESS = Argument(
    key="--task-address",
    last_injection_value="",
    metavar="bind",
    help="RPC server bind address.",
)
ARG_TASK_REGISTER = Argument(
    key="--task-register",
    last_injection_value="",
    metavar="key",
    help="Register key.",  # RSA public key
)

ARG_TASK_GROUP = Argument(
    key="--task-group",
    last_injection_value="",
    metavar="name",
    help="Group name",
)
ARG_TASK_PROJECT = Argument(
    key="--task-project",
    last_injection_value="",
    metavar="name",
    help="Project name",
)
ARG_TASK_NAME = Argument(
    key="--task-name",
    last_injection_value="",
    metavar="name",
    help="Task name",
)

ARG_TASK_WORKSPACE_DIR = Argument(
    key="--task-workspace-dir",
    last_injection_value="",
    metavar="dir",
    help="Task working directory.",
)
ARG_TASK_PACKAGE_DIR = Argument(
    key="--task-package-dir",
    last_injection_value="",
    metavar="dir",
    help="Task package directory.",
)
ARG_TASK_CACHE_DIR = Argument(
    key="--task-cache-dir",
    last_injection_value="",
    metavar="dir",
    help="Task cache directory.",
)

TASK_ARGS = (
    ARG_HELP,
    ARG_TASK_ADDRESS,
    ARG_TASK_REGISTER,
    ARG_TASK_GROUP,
    ARG_TASK_PROJECT,
    ARG_TASK_NAME,
    ARG_TASK_WORKSPACE_DIR,
    ARG_TASK_PACKAGE_DIR,
    ARG_TASK_CACHE_DIR,
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


def get_task_config_members(ignore_global_members=False) -> List[str]:
    members = [key for key, val in get_type_hints(TaskConfig).items()]
    if not ignore_global_members:
        return members
    global_members = get_global_config_members()
    return list(filter(lambda m: m not in global_members, members))
