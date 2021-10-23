# -*- coding: utf-8 -*-

from typing import Mapping, Text, Tuple, Any

assert_on_open = False
assert_on_close = False


async def on_open() -> None:
    global assert_on_open
    print("on_open")
    assert_on_open = True


async def on_close() -> None:
    global assert_on_close
    print("on_close")
    assert_on_close = True


async def on_packet(
    method: int,
    headers: Mapping[Text, Text],
    content: bytes,
) -> Tuple[int, Mapping[Text, Text], bytes]:
    print("on_packet")
    return method, headers, content


async def on_pickling(
    method: int,
    headers: Mapping[Text, Text],
    content: Any,
) -> Tuple[int, Mapping[Text, Text], Any]:
    print("on_pickling")
    return method, headers, content
