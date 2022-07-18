# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique
from socket import SOCK_DGRAM, SOCK_RAW, SOCK_STREAM
from typing import Optional, Union


@unique
class SockType(Enum):
    Unknown = 0
    Stream = 1  # TCP
    Dgram = 2  # UDP
    Raw = 3  # RAW


assert SockType.Stream.value == SOCK_STREAM
assert SockType.Dgram.value == SOCK_DGRAM
assert SockType.Raw.value == SOCK_RAW


@dataclass(init=False)
class Port:
    """It is mapped to the `port` table in the database."""

    number: int
    sock: SockType

    ref_uid: Optional[int]
    ref_category: Optional[str]

    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        number: int,
        sock: Union[SockType, int],
        ref_uid: Optional[int],
        ref_category: Optional[str],
        created_at: datetime,
        updated_at: datetime,
    ):
        self.number = number
        if isinstance(sock, SockType):
            self.sock = sock
        else:
            assert isinstance(sock, int)
            self.sock = SockType(sock)
        self.ref_uid = ref_uid
        self.ref_category = ref_category
        self.created_at = created_at
        self.updated_at = updated_at

    def is_tcp(self) -> bool:
        return self.sock == SockType.Stream

    def is_udp(self) -> bool:
        return self.sock == SockType.Dgram

    def is_raw(self) -> bool:
        return self.sock == SockType.Raw

    def is_allocated(self) -> bool:
        return self.ref_uid is not None and self.ref_category is not None

    def is_released(self) -> bool:
        return not self.is_allocated


class PortA(Port):
    pass


@dataclass
class PortRangeA:
    min: int
    max: int
