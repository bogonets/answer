# -*- coding: utf-8 -*-

from recc.argparse.config.global_config import create_usage, GlobalConfig
from recc.argparse.argument import Argument
from recc.argparse.command import Command

TASK_USAGE = create_usage(Command.task)
TASK_DESCRIPTION = "Task process"
TASK_EPILOG = ""

ARG_TASK_ADDRESS = Argument(
    key="--task-address",
    last_injection_value="",
    cls=str,
    metavar="bind",
    help="RPC server bind address.",
)
ARG_TASK_REGISTER = Argument(
    key="--task-register",
    last_injection_value="",
    cls=str,
    metavar="key",
    help="Register key.",  # RSA public key
)

ARG_TASK_GROUP = Argument(
    key="--task-group",
    last_injection_value="",
    cls=str,
    metavar="name",
    help="Group name",
)
ARG_TASK_PROJECT = Argument(
    key="--task-project",
    last_injection_value="",
    cls=str,
    metavar="name",
    help="Project name",
)
ARG_TASK_NAME = Argument(
    key="--task-name",
    last_injection_value="",
    cls=str,
    metavar="name",
    help="Task name",
)

ARG_TASK_WORKSPACE_DIR = Argument(
    key="--task-workspace-dir",
    last_injection_value="",
    cls=str,
    metavar="dir",
    help="Task working directory.",
)
ARG_TASK_PACKAGE_DIR = Argument(
    key="--task-package-dir",
    last_injection_value="",
    cls=str,
    metavar="dir",
    help="Task package directory.",
)
ARG_TASK_CACHE_DIR = Argument(
    key="--task-cache-dir",
    last_injection_value="",
    cls=str,
    metavar="dir",
    help="Task cache directory.",
)

TASK_ARGS = (
    ARG_TASK_ADDRESS,
    ARG_TASK_REGISTER,
    ARG_TASK_GROUP,
    ARG_TASK_PROJECT,
    ARG_TASK_NAME,
    ARG_TASK_WORKSPACE_DIR,
    ARG_TASK_PACKAGE_DIR,
    ARG_TASK_CACHE_DIR,
)


class TaskConfig(GlobalConfig):

    task_address: str
    task_register: str

    task_group: str
    task_project: str
    task_name: str

    task_workspace_dir: str
    task_package_dir: str
    task_cache_dir: str
