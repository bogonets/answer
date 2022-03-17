# -*- coding: utf-8 -*-

from argparse import Namespace
from recc.argparse.argument import Argument
from recc.argparse.command import Command
from recc.argparse.config.core_config import CoreConfig, CORE_ARGS
from recc.argparse.config.ctrl_config import CtrlConfig, CTRL_ARGS
from recc.argparse.config.task_config import TaskConfig, TASK_ARGS
from recc.argparse.config.daemon_config import DaemonConfig, DAEMON_ARGS
from recc.argparse.config.global_config import GlobalConfig, GLOBAL_ARGS
from recc.argparse.command import COMMAND_ARGUMENT_KEY


def get_default_namespace(*args: Argument) -> Namespace:
    result = Namespace()
    for arg in args:
        setattr(result, arg.normalize_key, arg.last_injection_value)
    return result


def get_default_global_namespace() -> Namespace:
    result = get_default_namespace(*GLOBAL_ARGS)
    setattr(result, COMMAND_ARGUMENT_KEY, Command.unknown.name)
    return result


def get_default_core_namespace() -> Namespace:
    result = get_default_namespace(*GLOBAL_ARGS, *CORE_ARGS)
    setattr(result, COMMAND_ARGUMENT_KEY, Command.core.name)
    return result


def get_default_ctrl_namespace() -> Namespace:
    result = get_default_namespace(*GLOBAL_ARGS, *CTRL_ARGS)
    setattr(result, COMMAND_ARGUMENT_KEY, Command.ctrl.name)
    return result


def get_default_task_namespace() -> Namespace:
    result = get_default_namespace(*GLOBAL_ARGS, *TASK_ARGS)
    setattr(result, COMMAND_ARGUMENT_KEY, Command.task.name)
    return result


def get_default_daemon_namespace() -> Namespace:
    result = get_default_namespace(*GLOBAL_ARGS, *DAEMON_ARGS)
    setattr(result, COMMAND_ARGUMENT_KEY, Command.daemon.name)
    return result


def get_default_global_config() -> GlobalConfig:
    return GlobalConfig(**vars(get_default_global_namespace()))


def get_default_core_config() -> CoreConfig:
    return CoreConfig(**vars(get_default_core_namespace()))


def get_default_ctrl_config() -> CtrlConfig:
    return CtrlConfig(**vars(get_default_ctrl_namespace()))


def get_default_task_config() -> TaskConfig:
    return TaskConfig(**vars(get_default_task_namespace()))


def get_default_daemon_config() -> DaemonConfig:
    return DaemonConfig(**vars(get_default_daemon_namespace()))
