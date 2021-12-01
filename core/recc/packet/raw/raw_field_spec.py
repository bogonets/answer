# -*- coding: utf-8 -*-

from typing import Optional, Iterable, Union
from random import randint
from recc.limit.integer import (
    BYTE_MIN,
    BYTE_MAX,
    UBYTE_MIN,
    UBYTE_MAX,
    SHORT_MIN,
    SHORT_MAX,
    USHORT_MIN,
    USHORT_MAX,
    LONG_MIN,
    LONG_MAX,
    ULONG_MIN,
    ULONG_MAX,
    LLONG_MIN,
    LLONG_MAX,
    ULLONG_MIN,
    ULLONG_MAX,
    min_signed,
    max_signed,
    max_unsigned,
)

BIG_ENDIAN = "big"
LITTLE_ENDIAN = "little"

DEFAULT_BYTEORDER_NAME = BIG_ENDIAN
DEFAULT_SIGNED = False


class RawFieldSpec:
    def __init__(
        self,
        name: str,
        size: int,
        value_range: Optional[Union[Iterable[int], range]] = None,
        byteorder=DEFAULT_BYTEORDER_NAME,
        signed=DEFAULT_SIGNED,
        *,
        range_sort=True,
    ):
        assert size >= 1
        assert byteorder in [BIG_ENDIAN, LITTLE_ENDIAN]

        self.name = name
        self.size = size

        self.range: Union[Iterable[int], range]
        if value_range is None:
            if size == 1:
                if signed:
                    self.range = range(BYTE_MIN, BYTE_MAX + 1)
                else:
                    self.range = range(UBYTE_MIN, UBYTE_MAX + 1)
            elif size == 2:
                if signed:
                    self.range = range(SHORT_MIN, SHORT_MAX + 1)
                else:
                    self.range = range(USHORT_MIN, USHORT_MAX + 1)
            elif size == 4:
                if signed:
                    self.range = range(LONG_MIN, LONG_MAX + 1)
                else:
                    self.range = range(ULONG_MIN, ULONG_MAX + 1)
            elif size == 8:
                if signed:
                    self.range = range(LLONG_MIN, LLONG_MAX + 1)
                else:
                    self.range = range(ULLONG_MIN, ULLONG_MAX + 1)
            else:
                if signed:
                    self.range = range(min_signed(size), max_signed(size) + 1)
                else:
                    self.range = range(0, max_unsigned(size) + 1)
        else:
            if isinstance(value_range, list):
                if range_sort:
                    self.range = sorted(set(value_range))
                else:
                    self.range = value_range
            else:
                assert isinstance(value_range, range)
                self.range = value_range

        self.byteorder = byteorder
        self.signed = signed

    def __contains__(self, item) -> bool:
        return item in self.range

    def __repr__(self) -> str:
        return f"RawFieldSpec(name={self.name},size={self.size}byte)"

    def __str__(self) -> str:
        return self.name

    @property
    def min(self) -> int:
        if isinstance(self.range, list):
            return self.range[0]
        else:
            assert isinstance(self.range, range)
            return self.range.start

    @property
    def max(self) -> int:
        if isinstance(self.range, list):
            return self.range[len(self.range) - 1]
        else:
            assert isinstance(self.range, range)
            return self.range.stop - 1

    def random(self) -> int:
        if isinstance(self.range, list):
            index = randint(0, len(self.range) - 1)
            return self.range[index]
        else:
            assert isinstance(self.range, range)
            return randint(self.range.start, self.range.stop - 1)
