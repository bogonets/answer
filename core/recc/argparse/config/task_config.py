# -*- coding: utf-8 -*-

from argparse import Namespace
from typing import Final, Optional, Any, List
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.argument import Shortcut, Argument
from recc.argparse.command import Command
from recc.argparse.config._utils import get_namespace, get_config_members


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
    default=None,
    metavar="bind",
    help="RPC server bind address.",
)
ARG_TASK_REGISTER = Argument(
    key="--task-register",
    last_injection_value="",
    default=None,
    metavar="key",
    help="Register key.",  # RSA public key
)

ARG_TASK_GROUP = Argument(
    key="--task-group",
    last_injection_value="",
    default=None,
    metavar="name",
    help="Group name",
)
ARG_TASK_PROJECT = Argument(
    key="--task-project",
    last_injection_value="",
    default=None,
    metavar="name",
    help="Project name",
)
ARG_TASK_NAME = Argument(
    key="--task-name",
    last_injection_value="",
    default=None,
    metavar="name",
    help="Task name",
)

ARG_TASK_WORKSPACE_DIR = Argument(
    key="--task-workspace-dir",
    last_injection_value="",
    default=None,
    metavar="dir",
    help="Task working directory.",
)
ARG_TASK_PACKAGE_DIR = Argument(
    key="--task-package-dir",
    last_injection_value="",
    default=None,
    metavar="dir",
    help="Task package directory.",
)
ARG_TASK_CACHE_DIR = Argument(
    key="--task-cache-dir",
    last_injection_value="",
    default=None,
    metavar="dir",
    help="Task cache directory.",
)

TASK_USAGE: Final[str] = f"recc {Command.task.name} [options]"
TASK_DESCRIPTION: Final[str] = "Task runner"
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
    return get_namespace(
        *cmdline,
        usage=TASK_USAGE,
        description=TASK_DESCRIPTION,
        arguments=TASK_ARGS,
        namespace=namespace,
    )


def cast_task_config(obj: Any) -> TaskConfig:
    return TaskConfig(**vars(obj))


def get_task_config(*cmdline: Any, namespace: Optional[Namespace] = None) -> TaskConfig:
    return cast_task_config(get_task_namespace(*cmdline, namespace))


def get_task_config_members(ignore_global_members=False) -> List[str]:
    return get_config_members(TaskConfig, ignore_global_members)
