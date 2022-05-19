# -*- coding: utf-8 -*-

from contextlib import contextmanager
from multiprocessing.shared_memory import SharedMemory
from typing import NamedTuple, Optional
from uuid import uuid4


class SharedMemoryTestInfo(NamedTuple):
    name: str
    data: str


# TODO: class SharedMemoryContext:


@contextmanager
def register_shared_memory(disable=False):
    sm: Optional[SharedMemory]

    if disable:
        test_sm_data = str()
        test_sm_pass_bytes = bytes()
        sm = None
        test_sm_name = str()
    else:
        test_sm_data = uuid4().hex
        test_sm_pass_bytes = bytes.fromhex(test_sm_data)
        sm = SharedMemory(create=True, size=len(test_sm_pass_bytes))
        test_sm_name = sm.name

    try:
        if sm:
            sm.buf[:] = test_sm_pass_bytes
        yield SharedMemoryTestInfo(test_sm_name, test_sm_data)
    finally:
        if sm:
            sm.close()
            sm.unlink()


def validate_shared_memory(name: str, data: str) -> bool:
    if name and data:
        try:
            sm = SharedMemory(name=name)
            try:
                return bytes(sm.buf[:]) == bytes.fromhex(data)
            finally:
                sm.close()
        except:  # noqa
            pass
    return False
