# -*- coding: utf-8 -*-

import os
import sys
from argparse import Namespace
from functools import lru_cache
from typing import Any, List, Optional, Union

from recc.argparse.argument_parser import ArgumentMessage, create_argument_parser
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
from recc.argparse.config.daemon_config import DaemonConfig
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.config.task_config import TaskConfig
from recc.argparse.config_file import read_config_file_if_readable
from recc.argparse.injection_values import injection_default_values
from recc.argparse.parser.env_parse import (
    get_namespace_by_os_env_files,
    get_namespace_by_os_envs,
)
from recc.filesystem.path_utils import get_home_dir
from recc.util.version import version_text
from recc.variables.argparse import (
    DEFAULT_CONFIG_FILENAME,
    GLOBAL_CONFIG_PATH,
    RECC_DOM_ROOT,
)
from recc.variables.environment import RECC_ENV_FILE_SUFFIX, RECC_ENV_PREFIX
from recc.variables.http import DEFAULT_HTTP_TEST_PORT
from recc.variables.plugin import TEST_CORE_PLUGIN_PREFIX, TEST_DAEMON_PLUGIN_PREFIX

ConfigType = Union[
    Namespace,
    GlobalConfig,
    CoreConfig,
    CtrlConfig,
    TaskConfig,
    DaemonConfig,
]


@lru_cache
def get_working_config_path() -> str:
    return os.path.join(os.getcwd(), DEFAULT_CONFIG_FILENAME)


@lru_cache
def get_home_config_path() -> str:
    return os.path.join(get_home_dir(), "." + DEFAULT_CONFIG_FILENAME)


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
    ignore_sys_argv=False,
    ignore_environment=False,
    ignore_default_paths=False,
    dom_root=RECC_DOM_ROOT,
) -> Namespace:
    if ignore_sys_argv:
        sys_argv = list()
    else:
        sys_argv = sys.argv[1:]

    args = cmdline if cmdline else sys_argv
    args = [str(a) for a in args if a is not None]

    # 1st: command-line arguments
    parser, helps, usages = create_argument_parser()

    # [IMPORTANT]
    # Do not use `namespace` parameter.
    # In the process of merging in the order `env -> cfg -> cmd`,
    # the `--verbose` option is `counted`, not `merge`.
    cmd_config, unrecognized_args = parser.parse_known_args(args, namespace=None)

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
        joins.append(read_config_file_if_readable(cmd_config.config, dom_root))

    env_config: Optional[Namespace]
    if ignore_environment:
        env_config = None
    else:
        env_config = get_namespace_by_os_envs(RECC_ENV_PREFIX)

    env_file_config: Optional[Namespace]
    if ignore_environment:
        env_file_config = None
    else:
        env_file_config = get_namespace_by_os_env_files(
            RECC_ENV_PREFIX, RECC_ENV_FILE_SUFFIX
        )

    # 3rd: environment config file
    if env_config and hasattr(env_config, "config"):
        joins.append(read_config_file_if_readable(env_config.config, dom_root))

    if not ignore_default_paths:
        # 4th: global config file
        joins.append(read_config_file_if_readable(GLOBAL_CONFIG_PATH, dom_root))

        # 5th: home config file
        joins.append(read_config_file_if_readable(get_home_config_path(), dom_root))

        # 6th: working config file
        joins.append(read_config_file_if_readable(get_working_config_path(), dom_root))

    if env_config:
        # 7th: environment variables
        joins.append(env_config)

    # 8th (last): environment variable pointing to file
    if env_file_config:
        joins.append(env_file_config)

    result = Namespace()
    left_join(result, *joins)

    # Last, default value.
    injection_default_values(result)

    return result


def parse_arguments_to_config(
    *cmdline: Any,
    ignore_sys_argv=False,
    ignore_environment=False,
    ignore_default_paths=False,
) -> ConfigType:
    result = parse_arguments_to_namespace(
        *cmdline,
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


def update_test_config(config: CoreConfig) -> CoreConfig:
    # GlobalConfig
    config.database_name = "recc.test"
    config.cache_prefix = "recc.test"
    config.skip_pip_download = True
    config.verbose = 0
    config.teardown = True
    config.developer = True
    # CoreConfig
    config.http_port = DEFAULT_HTTP_TEST_PORT
    config.public_signup = False
    config.core_plugin_prefix = TEST_CORE_PLUGIN_PREFIX
    config.daemon_plugin_prefix = TEST_DAEMON_PLUGIN_PREFIX
    return config
