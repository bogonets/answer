# -*- coding: utf-8 -*-

from argparse import Namespace

from recc.argparse.argument import Argument
from recc.argparse.command import COMMAND_ARGUMENT_KEY, Command
from recc.argparse.config.core_config import CORE_ARGS
from recc.argparse.config.ctrl_config import CTRL_ARGS
from recc.argparse.config.daemon_config import DAEMON_ARGS
from recc.argparse.config.global_config import GLOBAL_ARGS
from recc.argparse.config.task_config import TASK_ARGS


def injection_values_by_args(
    namespace: Namespace,
    *args: Argument,
) -> Namespace:
    for arg in args:
        arg.inject_to_namespace(namespace)
    return namespace


def cast_values_by_args_if_exists(
    namespace: Namespace,
    *args: Argument,
) -> Namespace:
    for arg in args:
        key = arg.normalize_key
        if not hasattr(namespace, key):
            continue

        val = getattr(namespace, key)
        if isinstance(val, arg.cls_origin):
            continue

        setattr(namespace, key, arg.cast(val))

    return namespace


def injection_global_default_values(namespace: Namespace) -> Namespace:
    return injection_values_by_args(namespace, *GLOBAL_ARGS)


def injection_core_default_values(namespace: Namespace) -> Namespace:
    return injection_values_by_args(namespace, *CORE_ARGS)


def injection_ctrl_default_values(namespace: Namespace) -> Namespace:
    return injection_values_by_args(namespace, *CTRL_ARGS)


def injection_task_default_values(namespace: Namespace) -> Namespace:
    return injection_values_by_args(namespace, *TASK_ARGS)


def injection_daemon_default_values(namespace: Namespace) -> Namespace:
    return injection_values_by_args(namespace, *DAEMON_ARGS)


def injection_default_values(namespace: Namespace) -> Namespace:
    injection_global_default_values(namespace)
    command = getattr(namespace, COMMAND_ARGUMENT_KEY)
    if command:
        if command == Command.core.name:
            return injection_core_default_values(namespace)
        elif command == Command.ctrl.name:
            return injection_ctrl_default_values(namespace)
        elif command == Command.task.name:
            return injection_task_default_values(namespace)
        elif command == Command.daemon.name:
            return injection_daemon_default_values(namespace)
    return namespace
