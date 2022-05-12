# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TaskA:
    key: str
    name: str
    status: str
    labels: Dict[str, str]
    ports: Dict[str, List[str]]
