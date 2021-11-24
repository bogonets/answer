# -*- coding: utf-8 -*-

from math import floor

BYTE_MIN = -128
BYTE_MAX = 127

UBYTE_MIN = 0
UBYTE_MAX = 255

SHORT_MIN = -32768
SHORT_MAX = 32767

USHORT_MIN = 0
USHORT_MAX = 65535

INT_MIN = -2147483648
INT_MAX = 2147483647

UINT_MIN = 0
UINT_MAX = 4294967295

LONG_MIN = -2147483648
LONG_MAX = 2147483647

ULONG_MIN = 0
ULONG_MAX = 4294967295

LLONG_MIN = -9223372036854775808
LLONG_MAX = 9223372036854775807

ULLONG_MIN = 0
ULLONG_MAX = 18446744073709551615


def min_signed(size: int) -> int:
    return -floor((2 ** (size * 8) / 2))


def max_signed(size: int) -> int:
    return floor((2 ** (size * 8) / 2)) - 1


def max_unsigned(size: int) -> int:
    return (2 ** (size * 8)) - 1
