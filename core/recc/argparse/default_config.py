# -*- coding: utf-8 -*-

from argparse import Namespace

from recc.argparse.argument import Argument
from recc.argparse.command import COMMAND_ARGUMENT_KEY, Command
from recc.argparse.config.core_config import CORE_ARGS, CoreConfig
from recc.argparse.config.global_config import GLOBAL_ARGS, GlobalConfig


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


def get_default_global_config() -> GlobalConfig:
    return GlobalConfig(**vars(get_default_global_namespace()))


def get_default_core_config() -> CoreConfig:
    return CoreConfig(**vars(get_default_core_namespace()))
