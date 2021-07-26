# -*- coding: utf-8 -*-

from typing import List, Dict


class ImageInfo:

    __slots__ = ("key", "tags", "labels")

    key: str
    tags: List[str]
    labels: Dict[str, str]

    def __init__(
        self,
        key: str,
        tags: List[str],
        labels: Dict[str, str],
    ):
        self.key = key
        self.tags = tags
        self.labels = labels
