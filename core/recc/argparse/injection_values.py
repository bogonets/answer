# -*- coding: utf-8 -*-

from argparse import Namespace
from recc.argparse.argument import Argument
from recc.argparse.config.core_config import CORE_ARGS
from recc.argparse.config.ctrl_config import CTRL_ARGS
from recc.argparse.config.task_config import TASK_ARGS
from recc.argparse.config.daemon_config import DAEMON_ARGS
from recc.argparse.config.global_config import GLOBAL_ARGS
from recc.argparse.command import Command, COMMAND_ARGUMENT_KEY


def injection_value_by_arg(namespace: Namespace, arg: Argument) -> Namespace:
    key = arg.normalize_key
    namespace_value = getattr(namespace, key, None)
    inference_type = arg.cls

    if namespace_value is None:
        default_value = arg.last_injection_value
        if default_value is not None:
            assert isinstance(default_value, inference_type)
        setattr(namespace, key, default_value)
    else:
        if not isinstance(namespace_value, inference_type):
            setattr(namespace, key, inference_type(namespace_value))

    return namespace


def injection_values_by_args(
    namespace: Namespace,
    *args: Argument,
) -> Namespace:
    for arg in args:
        injection_value_by_arg(namespace, arg)
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
        if isinstance(val, arg.cls):
            continue

        setattr(namespace, key, arg.cls(val))

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
