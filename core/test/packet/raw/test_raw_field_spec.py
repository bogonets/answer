# -*- coding: utf-8 -*-

from unittest import main, TestCase
from recc.packet.raw.raw_field_spec import RawFieldSpec
from recc.limit.integer import UBYTE_MIN, UBYTE_MAX, max_unsigned


class RawFieldSpecTestCase(TestCase):
    def test_min_max(self):
        a = RawFieldSpec("a", 1)
        self.assertEqual(a.min, UBYTE_MIN)
        self.assertEqual(a.max, UBYTE_MAX)

        b = RawFieldSpec("b", 3)
        self.assertEqual(b.min, 0)
        self.assertEqual(b.max, max_unsigned(3))

        c = RawFieldSpec("c", 2, range(0, 3))
        self.assertEqual(c.min, 0)
        self.assertEqual(c.max, 2)

        d = RawFieldSpec("d", 1, [1, 2, 4, 5])
        self.assertEqual(d.min, 1)
        self.assertEqual(d.max, 5)

        e = RawFieldSpec("c", 2, range(-10, 8), signed=True)
        self.assertEqual(e.min, -10)
        self.assertEqual(e.max, 7)

    def test_range_list(self):
        a = RawFieldSpec("a", 1, [5, 0, 1, 5, -4], range_sort=False)
        self.assertIsInstance(a.range, list)
        self.assertEqual(5, a.min)
        self.assertEqual(-4, a.max)

        b = RawFieldSpec("b", 1, [5, 0, 1, 8, 1, -4, 9, 2, 9, 8, 8, 10])
        self.assertIsInstance(b.range, list)
        self.assertEqual(-4, b.min)
        self.assertEqual(10, b.max)
        self.assertListEqual([-4, 0, 1, 2, 5, 8, 9, 10], b.range)


if __name__ == "__main__":
    main()
