# -*- coding: utf-8 -*-

import json  # [WARNING] Don't use any other `json` driver.
from argparse import Namespace
from recc.argparse.parser.dict_parse import get_namespace_by_dict


def get_namespace_by_json_text(json_text: str, *subsection_path: str) -> Namespace:
    return get_namespace_by_dict(json.loads(json_text), *subsection_path)


def get_namespace_by_json_path(
    json_path: str,
    *subsection_path: str,
    encoding="utf-8",
) -> Namespace:
    with open(json_path, encoding=encoding) as f:
        content = f.read()
    return get_namespace_by_json_text(content, *subsection_path)
