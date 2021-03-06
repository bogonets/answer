# -*- coding: utf-8 -*-

import os
from tempfile import gettempdir
from functools import lru_cache


@lru_cache
def get_home_dir() -> str:
    try:
        # Python 3.5+
        from pathlib import Path

        return str(Path.home())
    except ImportError:
        return os.path.expanduser("~")


HOME_DIR = get_home_dir()
TEMP_DIR = gettempdir()
