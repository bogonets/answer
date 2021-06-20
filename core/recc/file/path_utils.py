# -*- coding: utf-8 -*-

import os
import tempfile


def _get_home_dir() -> str:
    try:
        # Python 3.5+
        from pathlib import Path

        return str(Path.home())
    except ImportError:
        return os.path.expanduser("~")


HOME_DIR = _get_home_dir()
TEMP_DIR = tempfile.gettempdir()
