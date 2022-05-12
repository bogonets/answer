# -*- coding: utf-8 -*-

import os
from functools import lru_cache
from tempfile import gettempdir


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
