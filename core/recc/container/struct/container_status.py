# -*- coding: utf-8 -*-

from enum import Enum


class ContainerStatus(Enum):

    Created = 0
    Restarting = 1
    Running = 2
    Removing = 3
    Paused = 4
    Exited = 5
    Dead = 6

    @classmethod
    def from_str(cls, text: str):
        status_key = text[0].upper() + text[1:].lower()
        statuses = [s for s in dir(cls) if not s.startswith("_")]
        if status_key in statuses:
            return getattr(cls, status_key)
        raise KeyError(f"Not found '{status_key}' enum in {cls.__name__}")
