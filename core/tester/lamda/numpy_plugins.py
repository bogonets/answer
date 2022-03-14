# -*- coding: utf-8 -*-

import os
import shutil
from typing import List
from recc.filesystem.directory import prepare_directory
from recc.package.package_utils import get_module_directory
from recc.lamda_builtin import numpy as builtin_numpy


def _is_json(name: str) -> bool:
    return os.path.splitext(name)[1].lower() == ".json"


def copy_builtin_numpy_nodes(destination: str) -> List[str]:
    builtin_numpy_dir = get_module_directory(builtin_numpy)
    assert os.path.isdir(builtin_numpy_dir)
    numpy_files = os.listdir(builtin_numpy_dir)
    numpy_json_files = list(filter(_is_json, numpy_files))

    numpy_plugin_name = os.path.basename(builtin_numpy_dir)
    assert numpy_plugin_name == "numpy"
    numpy_plugin_dir = os.path.join(destination, numpy_plugin_name)
    shutil.copytree(builtin_numpy_dir, numpy_plugin_dir)

    # More samples.
    prepare_directory(os.path.join(numpy_plugin_dir, ".git"))
    prepare_directory(os.path.join(numpy_plugin_dir, "__pycache__"))

    return numpy_json_files
