# -*- coding: utf-8 -*-

import os
from functools import lru_cache

_TESTER_UNITTEST_DIR = os.path.dirname(__file__)
_TESTER_DIR = os.path.dirname(_TESTER_UNITTEST_DIR)
_CORE_DIR = os.path.dirname(_TESTER_DIR)
_CORE_STORAGE_DIR = os.path.join(_CORE_DIR, "storage")
_PIP_DOWNLOAD_DIR = os.path.join(_CORE_STORAGE_DIR, "pip.download")


@lru_cache
def get_pip_download_dir() -> str:
    if not os.path.exists(_CORE_STORAGE_DIR):
        os.mkdir(_CORE_STORAGE_DIR)
    if not os.path.exists(_PIP_DOWNLOAD_DIR):
        os.mkdir(_PIP_DOWNLOAD_DIR)

    assert os.path.isdir(_PIP_DOWNLOAD_DIR)
    assert os.access(_PIP_DOWNLOAD_DIR, os.W_OK)

    return _PIP_DOWNLOAD_DIR
