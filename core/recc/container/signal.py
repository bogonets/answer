# -*- coding: utf-8 -*-

from signal import Signals
from typing import Dict


def map_signum_to_name() -> Dict[int, str]:
    return {v.value: v.name for v in list(Signals)}


def map_name_to_signum() -> Dict[str, int]:
    return {v.name: v.value for v in list(Signals)}


SIGNUM_TO_NAME = map_signum_to_name()
NAME_TO_SIGNUM = map_name_to_signum()
