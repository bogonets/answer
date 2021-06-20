# -*- coding: utf-8 -*-

import os
from typing import Optional
from argparse import Namespace
from recc.argparse.parser.cfg_parse import get_namespace_by_cfg_path
from recc.argparse.parser.json_parse import get_namespace_by_json_path
from recc.argparse.parser.yaml_parse import get_namespace_by_yaml_path
from recc.file.permission import is_readable_file

CFG_EXTENSIONS = ("cfg", "ini")
JSON_EXTENSIONS = ("json",)
YAML_EXTENSIONS = ("yaml", "yml")


def normalize_extension(extension: str) -> str:
    stripped_ext = extension.strip()
    if stripped_ext[0] == ".":
        return stripped_ext[1:].lower()  # Remove Dot('.').
    else:
        return stripped_ext.lower()


def get_extension(path: str) -> str:
    return os.path.splitext(path)[1]


def read_config_file(
    path: str,
    *subsection_path: str,
    encoding="utf-8",
) -> Namespace:
    return read_config_file_with_extension(
        path, get_extension(path), *subsection_path, encoding=encoding
    )


def read_config_file_with_extension(
    path: str,
    extension: str,
    *subsection_path: str,
    encoding="utf-8",
) -> Namespace:
    if not path:
        raise ValueError("Emtpy `path` argument.")

    if not extension:
        raise ValueError("Emtpy `extension` argument.")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Not found config file: {path}")

    if not os.access(path, os.R_OK):
        raise PermissionError(f"The file cannot be accessed: {path}")

    comp_ext = normalize_extension(extension)

    if comp_ext in CFG_EXTENSIONS:
        if subsection_path:
            if len(subsection_path) >= 2:
                msg = f"{comp_ext} files do not allow subsections greater than 2-depth."
                raise IndexError(msg)
            section = subsection_path[0]
        else:
            section = str()
        return get_namespace_by_cfg_path(path, section, encoding=encoding)
    elif comp_ext in JSON_EXTENSIONS:
        return get_namespace_by_json_path(path, *subsection_path, encoding=encoding)
    elif comp_ext in YAML_EXTENSIONS:
        return get_namespace_by_yaml_path(path, *subsection_path, encoding=encoding)

    raise RuntimeError(f"Unsupported file extension: {extension}")


def read_config_file_safe(path: str, *subsection_path: str) -> Optional[Namespace]:
    if not path:
        return None
    try:
        if is_readable_file(path):
            return read_config_file(path, *subsection_path)
        else:
            return None
    except:  # noqa
        return None
