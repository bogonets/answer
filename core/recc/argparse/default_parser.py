# -*- coding: utf-8 -*-

import os
import sys
import pathlib
from argparse import Namespace
from typing import Optional, Any, Union, List
from recc.argparse.command import (
    COMMAND_ARGUMENT_KEY,
    HELP_ARGUMENT_KEY,
    SUBCOMMAND_HELP_ARGUMENT_KEY,
    VERSION_ARGUMENT_KEY,
    Command,
    get_available_commands,
)
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.config.ctrl_config import CtrlConfig
from recc.argparse.config.task_config import TaskConfig
from recc.argparse.config.daemon_config import DaemonConfig
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.config_file import read_config_file_safe
from recc.argparse.argument_parser import ArgumentMessage, create_argument_parser
from recc.argparse.parser.env_parse import get_namespace_by_os_envs
from recc.argparse.injection_values import injection_default_values
from recc.variables.environment import RECC_ENV_PREFIX
from recc.util.version import version_text

ConfigType = Union[
    Namespace,
    GlobalConfig,
    CoreConfig,
    CtrlConfig,
    TaskConfig,
    DaemonConfig,
]

CONFIG_FILENAME = "recc.cfg"
WORKING_CONFIG_PATH = os.path.join(os.getcwd(), CONFIG_FILENAME)
HOME_CONFIG_PATH = os.path.join(pathlib.Path.home(), "." + CONFIG_FILENAME)
GLOBAL_CONFIG_PATH = os.path.join("/etc", CONFIG_FILENAME)

RECC_DOM_ROOT = "recc"


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
    if not hasattr(obj, "command"):
        return None

    value = getattr(obj, "command", None)
    try:
        if not isinstance(value, str):
            raise TypeError
        return Command[value]
    except:  # noqa
        return Command.unknown


# def get_command_line_namespace(
#     *cmdline: Any,
#     namespace: Optional[Namespace] = None,
#     ignore_sys_argv=False,
# ) -> Namespace:
#     global_namespace, command_args = get_global_namespace_and_command_args(
#         *cmdline, namespace=namespace, ignore_sys_argv=ignore_sys_argv
#     )
#
#     cmd = get_command(global_namespace)
#     if cmd == Command.core:
#         return get_core_namespace(*command_args, namespace=global_namespace)
#     elif cmd == Command.ctrl:
#         return get_ctrl_namespace(*command_args, namespace=global_namespace)
#     elif cmd == Command.task:
#         return get_task_namespace(*command_args, namespace=global_namespace)
#     elif cmd == Command.daemon:
#         return get_daemon_namespace(*command_args, namespace=global_namespace)
#
#     assert cmd == Command.unknown
#     return global_namespace


def cast_config_type(namespace: Namespace) -> ConfigType:
    cmd = get_command(namespace)

    if cmd == Command.core:
        return CoreConfig(**vars(namespace))
    elif cmd == Command.ctrl:
        return CtrlConfig(**vars(namespace))
    elif cmd == Command.task:
        return TaskConfig(**vars(namespace))
    elif cmd == Command.daemon:
        return DaemonConfig(**vars(namespace))
    else:
        assert cmd == Command.unknown
        return GlobalConfig(**vars(namespace))


def parse_arguments_to_namespace(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
    ignore_sys_argv=False,
    ignore_environment=False,
    ignore_default_paths=False,
) -> Namespace:
    if ignore_sys_argv:
        sys_argv = list()
    else:
        sys_argv = sys.argv[1:]

    args = cmdline if cmdline else sys_argv
    args = [str(a) for a in args if a is not None]

    # 1st: command-line arguments
    parser, helps, usages = create_argument_parser()
    cmd_config, unrecognized_args = parser.parse_known_args(args, namespace)

    assert hasattr(cmd_config, COMMAND_ARGUMENT_KEY)
    assert hasattr(cmd_config, HELP_ARGUMENT_KEY)
    # `SUBCOMMAND_HELP_ARGUMENT_KEY` is Optional
    assert hasattr(cmd_config, VERSION_ARGUMENT_KEY)

    arg_command: Optional[str] = getattr(cmd_config, COMMAND_ARGUMENT_KEY)
    arg_help: bool = getattr(cmd_config, HELP_ARGUMENT_KEY)
    arg_version: bool = getattr(cmd_config, VERSION_ARGUMENT_KEY)
    arg_subcommand_help: bool = getattr(cmd_config, SUBCOMMAND_HELP_ARGUMENT_KEY, False)

    delattr(cmd_config, HELP_ARGUMENT_KEY)
    delattr(cmd_config, VERSION_ARGUMENT_KEY)
    if hasattr(cmd_config, SUBCOMMAND_HELP_ARGUMENT_KEY):
        delattr(cmd_config, SUBCOMMAND_HELP_ARGUMENT_KEY)

    assert isinstance(arg_help, bool)
    assert isinstance(arg_version, bool)
    assert isinstance(arg_subcommand_help, bool)

    if unrecognized_args:
        raise ArgumentMessage(f"Unrecognized arguments: {unrecognized_args}")

    if not arg_command:
        if arg_help:
            raise ArgumentMessage(helps[Command.unknown], 0)
        if arg_version:
            raise ArgumentMessage(version_text, 0)
        raise ArgumentMessage(usages[Command.unknown])

    if arg_command not in get_available_commands():
        raise ArgumentMessage(f"Unknown command: '{arg_command}'")

    if arg_version:
        raise ArgumentMessage("Global `--version` flags and subcommands cannot coexist")
    if arg_help:
        raise ArgumentMessage("Global `--help` flags and subcommands cannot coexist")

    command = Command[arg_command]

    if arg_subcommand_help:
        raise ArgumentMessage(helps[command], 0)

    joins: List[Optional[Namespace]] = [cmd_config]

    # 2nd: command-line config file
    if hasattr(cmd_config, "config"):
        joins.append(read_config_file_safe(cmd_config.config, RECC_DOM_ROOT))

    env_config: Optional[Namespace]
    if ignore_environment:
        env_config = None
    else:
        env_config = get_namespace_by_os_envs(RECC_ENV_PREFIX)

    # 3rd: environment config file
    if env_config and hasattr(env_config, "config"):
        joins.append(read_config_file_safe(env_config.config, RECC_DOM_ROOT))

    if not ignore_default_paths:
        # 4th: global config file
        joins.append(read_config_file_safe(GLOBAL_CONFIG_PATH, RECC_DOM_ROOT))

        # 5th: home config file
        joins.append(read_config_file_safe(HOME_CONFIG_PATH, RECC_DOM_ROOT))

        # 6th: working config file
        joins.append(read_config_file_safe(WORKING_CONFIG_PATH, RECC_DOM_ROOT))

    if env_config:
        # 7th: environment variables
        joins.append(env_config)

    # TODO: 8th (last): environment variables files

    result = Namespace()
    left_join(result, *joins)

    # Last, default value.
    injection_default_values(result)

    return result


def parse_arguments_to_config(
    *cmdline: Any,
    namespace: Optional[Namespace] = None,
    ignore_sys_argv=False,
    ignore_environment=False,
    ignore_default_paths=False,
) -> ConfigType:
    result = parse_arguments_to_namespace(
        *cmdline,
        namespace=namespace,
        ignore_sys_argv=ignore_sys_argv,
        ignore_environment=ignore_environment,
        ignore_default_paths=ignore_default_paths,
    )
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


def parse_arguments_to_core_config(
    global_options: Optional[List[Any]] = None,
    core_options: Optional[List[Any]] = None,
    **kwargs,
) -> CoreConfig:
    args = _none_optional_args(global_options, [Command.core.name], core_options)
    result = parse_arguments_to_config(*args, **kwargs)
    assert isinstance(result, CoreConfig)
    return result


def parse_arguments_to_ctrl_config(
    global_options: Optional[List[Any]] = None,
    ctrl_options: Optional[List[Any]] = None,
    **kwargs,
) -> CtrlConfig:
    args = _none_optional_args(global_options, [Command.ctrl.name], ctrl_options)
    result = parse_arguments_to_config(*args, **kwargs)
    assert isinstance(result, CtrlConfig)
    return result


def parse_arguments_to_task_config(
    global_options: Optional[List[Any]] = None,
    task_options: Optional[List[Any]] = None,
    **kwargs,
) -> TaskConfig:
    args = _none_optional_args(global_options, [Command.task.name], task_options)
    result = parse_arguments_to_config(*args, **kwargs)
    assert isinstance(result, TaskConfig)
    return result


def parse_arguments_to_daemon_config(
    global_options: Optional[List[Any]] = None,
    daemon_options: Optional[List[Any]] = None,
    **kwargs,
) -> DaemonConfig:
    args = _none_optional_args(global_options, [Command.daemon.name], daemon_options)
    result = parse_arguments_to_config(*args, **kwargs)
    assert isinstance(result, DaemonConfig)
    return result
