# -*- coding: utf-8 -*-

from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum


class ContainerOperator(Enum):

    Start = 0
    Stop = 1
    Kill = 2
    Restart = 3
    Pause = 4
    Resume = 5
    Remove = 6

    @classmethod
    def from_str(cls, text: str):
        operator_key = text[0].upper() + text[1:].lower()
        operators = [s for s in dir(cls) if not s.startswith("_")]
        if operator_key in operators:
            return getattr(cls, operator_key)
        raise KeyError(f"Not found '{operator_key}' enum in {cls.__name__}")


@dataclass
class ContainerA:
    key: str
    name: str
    status: str
    image: str
    created: str
    labels: Dict[str, str]
    ports: Dict[str, List[str]]


@dataclass
class ControlContainersQ:
    keys: List[str]
    operator: str
    signal: Optional[str] = None
    force: Optional[bool] = None
