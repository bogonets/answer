# -*- coding: utf-8 -*-

from recc.proto.daemon.daemon_api_pb2 import Content


def has_array(content: Content) -> bool:
    if not content.array:
        return False
    if not content.array.shape:
        return False
    if not content.array.dtype:
        return False
    if not content.array.strides:
        return False
    return True


def has_shared_memory(content: Content) -> bool:
    if not content.sm_name:
        return False
    assert content.size >= 0
    if content.size == 0:
        return False
    return True
