# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Pip:
    """It is mapped to the `pip` table in the database."""

    domain: str
    name: str
    file: str
    hash_method: str
    hash_value: str
