# -*- coding: utf-8 -*-

from unittest import main, TestCase
from recc.limit.integer import (
    BYTE_MIN,
    BYTE_MAX,
    UBYTE_MIN,
    UBYTE_MAX,
    SHORT_MIN,
    SHORT_MAX,
    USHORT_MIN,
    USHORT_MAX,
    INT_MIN,
    INT_MAX,
    UINT_MIN,
    UINT_MAX,
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


class IntegerTestCase(TestCase):
    def test_min_signed(self):
        self.assertEqual(BYTE_MIN, min_signed(1))
        self.assertEqual(SHORT_MIN, min_signed(2))
        self.assertEqual(INT_MIN, min_signed(4))
        self.assertEqual(LONG_MIN, min_signed(4))
        self.assertEqual(LLONG_MIN, min_signed(8))

    def test_max_signed(self):
        self.assertEqual(BYTE_MAX, max_signed(1))
        self.assertEqual(SHORT_MAX, max_signed(2))
        self.assertEqual(INT_MAX, max_signed(4))
        self.assertEqual(LONG_MAX, max_signed(4))
        self.assertEqual(LLONG_MAX, max_signed(8))

    def test_min_unsigned(self):
        self.assertEqual(UBYTE_MIN, 0)
        self.assertEqual(USHORT_MIN, 0)
        self.assertEqual(UINT_MIN, 0)
        self.assertEqual(ULONG_MIN, 0)
        self.assertEqual(ULLONG_MIN, 0)

    def test_max_unsigned(self):
        self.assertEqual(UBYTE_MAX, max_unsigned(1))
        self.assertEqual(USHORT_MAX, max_unsigned(2))
        self.assertEqual(UINT_MAX, max_unsigned(4))
        self.assertEqual(ULONG_MAX, max_unsigned(4))
        self.assertEqual(ULLONG_MAX, max_unsigned(8))


if __name__ == "__main__":
    main()
