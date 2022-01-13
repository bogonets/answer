# -*- coding: utf-8 -*-

from typing import Dict, List, Any, Optional
from dataclasses import dataclass

assert_on_open = False
assert_on_close = False


async def on_open() -> None:
    global assert_on_open
    assert_on_open = True


async def on_close() -> None:
    global assert_on_close
    assert_on_close = True


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


async def put_test_body(body: _Test1):
    return _Test1(
        body.value1,
        body.value2,
        body.value3,
        body.value4,
        body.value5,
        body.value6,
    )


def on_routes():
    return [
        ("GET", "/test", get_test),
        ("GET", "/test/{value}/path", get_test_value_path),
        ("POST", "/test/{value}/path", post_test_value_path),
        ("PUT", "/test/body", put_test_body),
    ]
