# -*- coding: utf-8 -*-

from typing import Optional
from recc.argparse.config.global_config import (
    LOOP_DRIVER_UV,
    JSON_DRIVER_ORJSON,
    XML_DRIVER_XMLTODICT,
    YAML_DRIVER_PYYAML,
)
from recc.file.permission import is_readable_file
from recc.logging.logging import recc_common_logger as logger
from recc.logging.logging import (
    set_basic_config,
    set_root_level,
    convert_printable_level,
    set_default_logging_config,
    set_simple_logging_config,
)
from recc.driver.loop import install_uvloop_driver
from recc.driver.json import install_orjson_driver
from recc.driver.xml import install_xmltodict_driver
from recc.driver.yaml import install_pyyaml_driver


def init_logger(
    config_path: str,
    log_level: Optional[str] = None,
    simply=False,
) -> None:
    log_configurable: bool
    if simply:
        log_configurable = False
        set_simple_logging_config()
    else:
        log_configurable = bool(config_path and is_readable_file(config_path))
        if log_configurable:
            set_basic_config(config_path)
        else:
            set_default_logging_config()

    if log_level:
        set_root_level(log_level)

    # The resulting output should be after the logger setup is done.
    if log_configurable:
        logger.info(f"Initialize log config: {config_path}")
    if log_level:
        logger.info(f"Change root log level: {convert_printable_level(log_level)}")


def init_simple_logger(log_level: Optional[str] = None) -> None:
    set_simple_logging_config()
    if log_level:
        set_root_level(log_level)

    # The resulting output should be after the logger setup is done.
    if log_level:
        logger.info(f"Change root log level: {convert_printable_level(log_level)}")


def init_json_driver(json_type=JSON_DRIVER_ORJSON) -> None:
    if json_type == JSON_DRIVER_ORJSON:
        if install_orjson_driver():
            logger.info("Installed orjson json parser.")
        else:
            logger.warning("The orjson module doesn't exist.")
    else:
        logger.info("Using the default json parser.")


def init_xml_driver(xml_type=XML_DRIVER_XMLTODICT) -> None:
    if xml_type == XML_DRIVER_XMLTODICT:
        if install_xmltodict_driver():
            logger.info("Installed xmltodict xml parser.")
        else:
            logger.warning("The xmltodict module doesn't exist.")
    else:
        logger.info("Using the default xml parser.")


def init_yaml_driver(yaml_type=YAML_DRIVER_PYYAML) -> None:
    if yaml_type == YAML_DRIVER_PYYAML:
        if install_pyyaml_driver():
            logger.info("Installed PyYaml yaml parser.")
        else:
            logger.warning("The PyYaml module doesn't exist.")
    else:
        logger.info("Using the default yaml parser.")


def init_loop_driver(loop_type=LOOP_DRIVER_UV) -> None:
    if loop_type == LOOP_DRIVER_UV:
        if install_uvloop_driver():
            logger.info("Installed uvloop event loop.")
        else:
            logger.warning("The uvloop module doesn't exist.")
    else:
        logger.info("Using the default asyncio loop.")
