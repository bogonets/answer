# -*- coding: utf-8 -*-

import sys
from copy import deepcopy
from typing import List, Optional


class PathContext:

    original_path: Optional[List[str]]
    request_path: List[str]

    def __init__(self, *path: str, insert_operation=False):
        self.original_path = None
        self.request_path = deepcopy(list(path))
        self.insert_operation = insert_operation

    def open(self) -> None:
        self.original_path = deepcopy(sys.path)
        if self.insert_operation:
            for path in self.request_path:
                sys.path.insert(0, path)
        else:
            sys.path += self.request_path

    def close(self) -> None:
        assert self.original_path is not None
        sys.path = self.original_path
        self.original_path = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
