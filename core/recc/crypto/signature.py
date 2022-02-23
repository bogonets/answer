# -*- coding: utf-8 -*-

import os


def generate_signature(size: int) -> str:
    return os.urandom(size).hex()
