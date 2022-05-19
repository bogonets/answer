# -*- coding: utf-8 -*-

import os
from typing import Final

CURRENT_DIR: Final[str] = os.path.dirname(__file__)
DEFAULT_ENCODING: Final[str] = "utf-8"


def read_plugin(filename: str, encoding=DEFAULT_ENCODING) -> str:
    filepath = os.path.abspath(os.path.join(CURRENT_DIR, filename))
    with open(filepath, "r", encoding=encoding) as f:
        return f.read()


def copy_plugin(
    plugin_name: str,
    plugin_root_directory: str,
    encoding=DEFAULT_ENCODING,
) -> str:
    plugin_dir = os.path.join(plugin_root_directory, plugin_name)
    if not os.path.isdir(plugin_dir):
        os.mkdir(plugin_dir)

    plugin_filename = plugin_name + ".py"
    plugin_content = read_plugin(plugin_filename, encoding)
    destination_path = os.path.join(plugin_dir, "__init__.py")

    with open(destination_path, "w", encoding=encoding) as f:
        f.write(plugin_content)

    return destination_path
