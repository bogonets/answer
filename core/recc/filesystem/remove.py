# -*- coding: utf-8 -*-

import os


def remove_recursively(path: str) -> None:
    if os.path.isdir(path):
        for name in os.listdir(path):
            remove_recursively(os.path.join(path, name))
        os.rmdir(path)
    else:
        os.remove(path)
