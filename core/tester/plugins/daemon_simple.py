# -*- coding: utf-8 -*-

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from numpy import ndarray

# from recc.util.version import version_text
# print(version_text)
# import os
# print(os.environ["PYTHONPATH"])
# import sys
# print(sys.path)

assert_on_open = False
assert_on_close = False
assert_on_register = False
assert_main = False


async def on_open() -> None:
    global assert_on_open
    assert_on_open = True


async def on_close() -> None:
    global assert_on_close
    assert_on_close = True


async def on_register() -> None:
    global assert_on_register
    assert_on_register = True


async def get_test():
    pass


async def get_test_value_path(value: int):
    return value


async def post_test_value_path(value: str):
    return value


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


async def put_test_body(body: _Test1):
    return _Test1(
        body.value1,
        body.value2,
        body.value3,
        body.value4,
        body.value5,
        body.value6,
    )


class _TestException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


async def get_exception():
    raise _TestException()


async def post_test_numpy(array: ndarray) -> ndarray:
    result = array.copy()
    result.fill(0)
    return result


@dataclass
class _Result1:
    value1: int
    value2: str


async def patch_test_numpy_body(
    array: ndarray, body: _Test1
) -> Tuple[ndarray, _Result1]:
    result = array.copy()
    result.fill(0)
    return result, _Result1(body.value1, body.value2)


async def patch_test_numpy_body2(body: _Test2) -> Tuple[ndarray, _Result1]:
    isinstance(body, dict)
    result = body.array.copy()
    result.fill(0)
    return result, _Result1(body.body.value1, body.body.value2)


def on_routes():
    return [
        ("GET", "/test", get_test),
        ("GET", "/test/{value}/path", get_test_value_path),
        ("POST", "/test/{value}/path", post_test_value_path),
        ("PUT", "/test/body", put_test_body),
        ("GET", "/test/exception", get_exception),
        ("POST", "/test/numpy", post_test_numpy),
        ("PATCH", "/test/numpy/body", patch_test_numpy_body),
        ("PATCH", "/test/numpy/body2", patch_test_numpy_body2),
    ]


if __name__ == "__main__":
    assert_main = True
