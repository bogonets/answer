# -*- coding: utf-8 -*-

from configparser import ConfigParser  # [WARNING] Don't use any other `cfg` driver.
from typing import Optional, Dict, Any
from argparse import Namespace
from recc.argparse.parser.dict_parse import get_namespace_by_dict


def config_parser_to_dict(parser: ConfigParser) -> Dict[str, Dict[str, Any]]:
    result = dict()
    for section in parser.sections():
        section_result = dict()
        for option in parser.options(section):
            value = parser.get(section, option)
            section_result[option] = value
        result[section] = section_result
    return result


def get_namespace_by_parser(
    parser: ConfigParser,
    section: Optional[str] = None,
) -> Namespace:
    return get_namespace_by_dict(config_parser_to_dict(parser), section)


def get_namespace_by_cfg_text(
    cfg_text: str,
    section: Optional[str] = None,
) -> Namespace:
    parser = ConfigParser()
    parser.read_string(cfg_text)
    return get_namespace_by_parser(parser, section)


def get_namespace_by_cfg_path(
    cfg_path: str,
    section: Optional[str] = None,
    *,
    encoding="utf-8",
) -> Namespace:
    parser = ConfigParser()
    parser.read(cfg_path, encoding=encoding)
    return get_namespace_by_parser(parser, section)
