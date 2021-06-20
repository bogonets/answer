# -*- coding: utf-8 -*-

import yaml  # [WARNING] Don't use any other `yaml` driver.
from argparse import Namespace
from recc.argparse.parser.dict_parse import get_namespace_by_dict


def get_namespace_by_yaml_text(yaml_text: str, *subsection_path: str) -> Namespace:
    return get_namespace_by_dict(yaml.full_load(yaml_text), *subsection_path)


def get_namespace_by_yaml_path(
    yaml_path: str,
    *subsection_path: str,
    encoding="utf-8",
) -> Namespace:
    with open(yaml_path, encoding=encoding) as f:
        content = f.read()
    return get_namespace_by_yaml_text(content, *subsection_path)
