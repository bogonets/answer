# -*- coding: utf-8 -*-

from argparse import Namespace
from recc.argparse.argument import Argument
from recc.argparse.command import Command
from recc.argparse.config.core_config import (
    CoreConfig,
    CORE_ARGS,
    cast_core_config,
)
from recc.argparse.config.task_config import (
    TaskConfig,
    TASK_ARGS,
    cast_task_config,
)
from recc.argparse.config.global_config import (
    GlobalConfig,
    ARG_COMMAND,
    GLOBAL_ARGS,
    cast_global_config,
)


def get_default_namespace(*args: Argument) -> Namespace:
    result = Namespace()
    for arg in args:
        setattr(result, arg.normalize_key, arg.inference_default_value())
    return result


def get_default_global_namespace() -> Namespace:
    result = get_default_namespace(*GLOBAL_ARGS)
    setattr(result, ARG_COMMAND.normalize_key, Command.unknown.name)
    return result


def get_default_core_namespace() -> Namespace:
    result = get_default_namespace(*GLOBAL_ARGS, *CORE_ARGS)
    setattr(result, ARG_COMMAND.normalize_key, Command.core.name)
    return result


def get_default_task_namespace() -> Namespace:
    result = get_default_namespace(*GLOBAL_ARGS, *TASK_ARGS)
    setattr(result, ARG_COMMAND.normalize_key, Command.task.name)
    return result


def get_default_global_config() -> GlobalConfig:
    return cast_global_config(get_default_global_namespace())


def get_default_core_config() -> CoreConfig:
    return cast_core_config(get_default_core_namespace())


def get_default_task_config() -> TaskConfig:
    return cast_task_config(get_default_task_namespace())
