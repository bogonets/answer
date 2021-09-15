# -*- coding: utf-8 -*-

from dataclasses import dataclass

DEFAULT_VALUE = 0


@dataclass
class DataClassTester:
    key: str
    val: int = DEFAULT_VALUE


def on_create(context, **kwargs) -> None:
    pass


def on_destroy() -> None:
    pass


async def on_open() -> None:
    pass


async def on_close() -> None:
    pass
