# -*- coding: utf-8 -*-

from argparse import Namespace
from unittest import TestCase, main

from recc.argparse.default_parser import left_join


class DefaultParserTestCase(TestCase):
    def test_left_join_for_empty_object(self):
        name1 = Namespace(a=1, b=2)
        name2 = Namespace(c=3, d=4)

        result = Namespace()
        left_join(result, Namespace(), name1, None, name2, None, Namespace())
        self.assertEqual(4, len(vars(result)))
        self.assertEqual(1, result.a)
        self.assertEqual(2, result.b)
        self.assertEqual(3, result.c)
        self.assertEqual(4, result.d)

    def test_left_join_for_normal(self):
        name1 = Namespace(a=1, b=2)
        name2 = Namespace(c=3, d=4)
        name3 = Namespace(a=5, c=6)

        result = Namespace()
        left_join(result, name1, name2, name3)
        self.assertEqual(4, len(vars(result)))
        self.assertEqual(1, result.a)
        self.assertEqual(2, result.b)
        self.assertEqual(3, result.c)
        self.assertEqual(4, result.d)

    def test_left_join_for_none_merge(self):
        name1 = Namespace(a=None, b=2, c=3)
        name2 = Namespace(a=1, b=None, c=4)

        result = Namespace()
        left_join(result, name1, name2)
        self.assertEqual(3, len(vars(result)))
        self.assertEqual(1, result.a)
        self.assertEqual(2, result.b)
        self.assertEqual(3, result.c)


if __name__ == "__main__":
    main()
