# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from numpy import ndarray

__version__ = "0.0.0"


async def on_register(*args, **kwargs) -> int:
    assert args is not None
    assert kwargs is not None
    return 0


@dataclass
class _Test1:
    value1: int
    value2: str
    value3: Dict[str, int]
    value4: List[Any]
    value5: Optional[str] = None
    value6: Optional[List[int]] = None


@dataclass
class _Test2:
    array: ndarray
    body: _Test1


@dataclass
class _Result1:
    value1: int
    value2: str


async def patch_performance1(array: ndarray, body: _Test1) -> Tuple[ndarray, _Result1]:
    result = array.copy()
    result.fill(0)
    return result, _Result1(body.value1, body.value2)


async def patch_performance2(body: _Test2) -> Tuple[ndarray, _Result1]:
    isinstance(body, dict)
    result = body.array.copy()
    result.fill(0)
    return result, _Result1(body.body.value1, body.body.value2)


def on_routes():
    return [
        ("PATCH", "/performance1", patch_performance1),
        ("PATCH", "/performance2", patch_performance2),
    ]
