# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.limit.integer import (
    BYTE_MAX,
    BYTE_MIN,
    INT_MAX,
    INT_MIN,
    LLONG_MAX,
    LLONG_MIN,
    LONG_MAX,
    LONG_MIN,
    SHORT_MAX,
    SHORT_MIN,
    UBYTE_MAX,
    UBYTE_MIN,
    UINT_MAX,
    UINT_MIN,
    ULLONG_MAX,
    ULLONG_MIN,
    ULONG_MAX,
    ULONG_MIN,
    USHORT_MAX,
    USHORT_MIN,
    max_signed,
    max_unsigned,
    min_signed,
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
