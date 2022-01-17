# -*- coding: utf-8 -*-

import os
import json
from typing import Final, Any

CURRENT_DIR: Final[str] = os.path.dirname(__file__)
DEFAULT_ENCODING: Final[str] = "utf-8"


def get_sample_abspath(filename: str) -> str:
    return os.path.abspath(os.path.join(CURRENT_DIR, filename))


def read_sample(filename: str, encoding=DEFAULT_ENCODING) -> str:
    with open(get_sample_abspath(filename), "r", encoding=encoding) as f:
        return f.read()


def read_sample_json(filename: str, encoding=DEFAULT_ENCODING) -> Any:
    return json.loads(read_sample(filename, encoding))
