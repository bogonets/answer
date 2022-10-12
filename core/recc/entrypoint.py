# -*- coding: utf-8 -*-

from argparse import Namespace

from generalize_config import (
    merge_left_first,
    read_config_file,
    read_os_envs,
    read_os_envs_file,
)
from type_serialize import deserialize

from recc.arguments import default_argument_parser
from recc.config import Config
from recc.core.context import Context
from recc.http.http_app import HttpApp
from recc.logging.logging import recc_logger as logger


def read_configs() -> Config:
    cmds = default_argument_parser().parse_known_args()[0]
    assert hasattr(cmds, "config")
    cmd_config = read_config_file(cmds.config) if cmds.config else None
    envs = read_os_envs(prefix="RECC_")
    envs_config = read_config_file(envs.config) if hasattr(envs, "config") else None
    env_files_args = read_os_envs_file(prefix="RECC_", suffix="_FILE")
    default_args = Config.default()

    nss = (cmds, cmd_config, envs, envs_config, env_files_args, default_args)
    result_args = merge_left_first(Namespace(), *nss)
    config = deserialize(result_args, Config)

    assert isinstance(config, Config)
    config.assertion()

    return config


def main() -> int:
    """
    The entry point for the core project.
    """

    config = read_configs()
    logger.debug(f"Configuration: {config}")

    context = Context(config)
    app = HttpApp(context)

    try:
        app.run_until_complete()
    except BaseException as e:
        logger.exception(e)
        return 1
    else:
        return 0


if __name__ == "__main__":
    exit(main())
