# -*- coding: utf-8 -*-

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class TaskA:
    key: str
    name: str
    status: str
    labels: Dict[str, str]
    ports: Dict[str, List[str]]
