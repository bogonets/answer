# -*- coding: utf-8 -*-

from typing import Dict


class VolumeInfo:

    __slots__ = ("key", "name", "labels")

    key: str
    name: str
    labels: Dict[str, str]

    def __init__(
        self,
        key: str,
        name: str,
        labels: Dict[str, str],
    ):
        self.key = key
        self.name = name
        self.labels = labels
