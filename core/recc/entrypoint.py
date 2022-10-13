# -*- coding: utf-8 -*-

from argparse import Namespace
from asyncio import set_event_loop_policy

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
from recc.logging.logging import (
    set_basic_config,
    set_default_logging_config,
    set_root_level,
    set_simple_logging_config,
)


def install_uvloop_driver() -> None:
    try:
        import uvloop

        # Setup uvloop policy, so that every
        # asyncio.get_event_loop() will create an instance
        # of uvloop event loop.
        set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        logger.warning("Not found uvloop module")
    except BaseException as e:
        logger.warning(f"uvloop installation failed: {e}")
    else:
        logger.info("Install the event loop policy as uvloop")


def read_configs(env_prefix="RECC_", env_suffix="_FILE", config_key="config") -> Config:
    cmds = default_argument_parser().parse_known_args()[0]
    assert hasattr(cmds, config_key)
    cmd_config = read_config_file(cmds.config) if cmds.config else None
    envs = read_os_envs(prefix=env_prefix)
    envs_config = read_config_file(envs.config) if hasattr(envs, config_key) else None
    env_files_args = read_os_envs_file(prefix=env_prefix, suffix=env_suffix)
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

    if config.log_simply or config.log_config:
        raise ValueError(
            "Among the set variables, 'log_simply' and 'log_config' cannot coexist"
        )

    if config.log_simply:
        assert not config.log_config
        set_simple_logging_config()
    elif config.log_config:
        assert not config.log_simply
        set_basic_config(config.log_config)
    else:
        assert not config.log_config
        assert not config.log_simply
        set_default_logging_config()

    assert config.log_level
    set_root_level(config.log_level)

    logger.debug(f"Configuration result: {config}")

    if config.install_uvloop:
        install_uvloop_driver()

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
