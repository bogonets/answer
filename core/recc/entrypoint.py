# -*- coding: utf-8 -*-

from asyncio import set_event_loop_policy

from generalize_config import read_generalize_configs
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


def main() -> int:
    """
    The entry point for the core project.
    """

    args = read_generalize_configs(
        parser=default_argument_parser(),
        subsection="recc",
        env_prefix="RECC_",
        env_suffix="_FILE",
        config_key="config",
        force=None,
        default=Config.default(),
    )
    config = deserialize(args, Config)

    assert isinstance(config, Config)
    config.assertion()

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
