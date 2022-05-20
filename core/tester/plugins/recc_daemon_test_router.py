# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from numpy import ndarray

__version__ = "0.0.0"


class _TestException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


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


async def on_register(*args, **kwargs) -> int:
    assert args is not None
    assert kwargs is not None
    return 0


async def get_test():
    pass


async def get_test_value_path(value: int):
    return value


async def post_test_value_path(value: str):
    return value


async def put_test_body(body: _Test1):
    return _Test1(
        body.value1,
        body.value2,
        body.value3,
        body.value4,
        body.value5,
        body.value6,
    )


async def get_exception():
    raise _TestException()


async def post_test_numpy(array: ndarray) -> ndarray:
    result = array.copy()
    result.fill(0)
    return result


async def patch_test_numpy_body(
    array: ndarray, body: _Test1
) -> Tuple[ndarray, _Result1]:
    result = array.copy()
    result.fill(0)
    return result, _Result1(body.value1, body.value2)


def on_routes():
    return [
        ("GET", "/test", get_test),
        ("GET", "/test/{value}/path", get_test_value_path),
        ("POST", "/test/{value}/path", post_test_value_path),
        ("PUT", "/test/body", put_test_body),
        ("GET", "/test/exception", get_exception),
        ("POST", "/test/numpy", post_test_numpy),
        ("PATCH", "/test/numpy/body", patch_test_numpy_body),
    ]
