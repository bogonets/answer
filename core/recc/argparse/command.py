# -*- coding: utf-8 -*-

from enum import Enum
from typing import List


class Command(Enum):
    unknown = 0
    core = 1
    task = 2


def get_available_commands() -> List[str]:
    return [n for n, _ in Command.__members__.items() if n != Command.unknown.name]
