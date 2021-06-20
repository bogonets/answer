# -*- coding: utf-8 -*-

import os
import pathlib
from argparse import Namespace
from typing import Optional, Any, Union, List
from recc.argparse.command import Command
from recc.argparse.config.core_config import (
    CoreConfig,
    get_core_namespace,
    cast_core_config,
)
from recc.argparse.config.task_config import (
    TaskConfig,
    get_task_namespace,
    cast_task_config,
)
from recc.argparse.config.global_config import (
    GlobalConfig,
    ARG_COMMAND,
    get_global_namespace_and_command_args,
    cast_global_config,
)
from recc.argparse.config_file import read_config_file_safe
from recc.argparse.parser.env_parse import get_namespace_by_os_envs
from recc.argparse.injection_values import injection_default_values

ConfigType = Union[Namespace, GlobalConfig, CoreConfig, TaskConfig]

CONFIG_FILENAME = "recc.cfg"
WORKING_CONFIG_PATH = os.path.join(os.getcwd(), CONFIG_FILENAME)
HOME_CONFIG_PATH = os.path.join(pathlib.Path.home(), "." + CONFIG_FILENAME)
GLOBAL_CONFIG_PATH = os.path.join("/etc", CONFIG_FILENAME)

RECC_DOM_ROOT = "recc"
RECC_ENV_PREFIX = "RECC_"


def left_join(left: Namespace, *namespaces: Optional[Namespace]) -> Namespace:
    if not namespaces:
        return left
    for ns in namespaces:
        if not ns:
            continue
        for key in vars(ns):
            val = getattr(ns, key)
            if getattr(left, key, None) is None:
                setattr(left, key, val)
    return left


def get_command(obj: Namespace) -> Optional[Command]:
    if not hasattr(obj, ARG_COMMAND.normalize_key):
        return None

    value = getattr(obj, ARG_COMMAND.normalize_key, None)
    try:
        return Command[value]
    except:  # noqa
        return Command.unknown


def get_command_line_namespace(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
    ignore_sys_argv=False,
) -> Namespace:
    global_namespace, command_args = get_global_namespace_and_command_args(
        *cmdline, namespace=namespace, ignore_sys_argv=ignore_sys_argv
    )

    cmd = get_command(global_namespace)
    if cmd == Command.core:
        return get_core_namespace(*command_args, namespace=global_namespace)
    elif cmd == Command.task:
        return get_task_namespace(*command_args, namespace=global_namespace)

    assert cmd == Command.unknown
    return global_namespace


def cast_config_type(namespace: Namespace) -> ConfigType:
    cmd = get_command(namespace)
    if cmd == Command.core:
        return cast_core_config(namespace)
    elif cmd == Command.task:
        return cast_task_config(namespace)

    assert cmd == Command.unknown
    return cast_global_config(namespace)


def parse_arguments_to_namespace(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
    ignore_sys_argv=False,
    ignore_environment=False,
    ignore_default_paths=False,
) -> Namespace:
    # 1st: command-line arguments
    cmd_config = get_command_line_namespace(
        *cmdline, namespace=namespace, ignore_sys_argv=ignore_sys_argv
    )
    joins: List[Optional[Namespace]] = [cmd_config]

    # 2nd: command-line config file
    if hasattr(cmd_config, "config"):
        joins.append(read_config_file_safe(cmd_config.config, RECC_DOM_ROOT))

    if not ignore_environment:
        # 3rd: environment variables
        env_config = get_namespace_by_os_envs(RECC_ENV_PREFIX)
        joins.append(env_config)

        # 4th: environment config file
        if hasattr(env_config, "config"):
            joins.append(read_config_file_safe(env_config.config, RECC_DOM_ROOT))

    if not ignore_default_paths:
        # 5th: working config file
        joins.append(read_config_file_safe(WORKING_CONFIG_PATH, RECC_DOM_ROOT))

        # 6th: home config file
        joins.append(read_config_file_safe(HOME_CONFIG_PATH, RECC_DOM_ROOT))

        # 7th: global config file
        joins.append(read_config_file_safe(GLOBAL_CONFIG_PATH, RECC_DOM_ROOT))

    result = Namespace()
    left_join(result, *joins)

    # Last, default value.
    injection_default_values(result)

    return result


def parse_arguments_to_config(*args, **kwargs) -> ConfigType:
    result = parse_arguments_to_namespace(*args, **kwargs)
    return cast_config_type(result)


def _none_optional_args(*args_list: Optional[List[Any]]) -> List[str]:
    result: List[Any] = list()
    if not args_list:
        return result

    for args in args_list:
        if not args:
            continue
        assert isinstance(args, list)
        result += args

    return [str(i) for i in result if i]


def parse_arguments_to_config2(
    cmdline: Optional[List[Any]] = None,
    **kwargs,
) -> ConfigType:
    return parse_arguments_to_config(*_none_optional_args(cmdline), **kwargs)


def parse_arguments_to_core_config(
    global_options: Optional[List[Any]] = None,
    core_options: Optional[List[Any]] = None,
    **kwargs,
) -> CoreConfig:
    args = _none_optional_args(global_options, [Command.core.name], core_options)
    result = parse_arguments_to_config2(args, **kwargs)
    assert isinstance(result, CoreConfig)
    return result


def parse_arguments_to_task_config(
    global_options: Optional[List[Any]] = None,
    task_options: Optional[List[Any]] = None,
    **kwargs,
) -> TaskConfig:
    args = _none_optional_args(global_options, [Command.core.name], task_options)
    result = parse_arguments_to_config2(args, **kwargs)
    assert isinstance(result, TaskConfig)
    return result
