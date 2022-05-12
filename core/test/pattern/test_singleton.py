# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.pattern.singleton import singleton


@singleton
class _TestSingleton:
    def __init__(self):
        self.value = 0


class SingletonTestCase(TestCase):
    def test_default(self):
        a = _TestSingleton()
        b = _TestSingleton()
        self.assertEqual(id(a), id(b))
        self.assertEqual(0, a.value)
        self.assertEqual(0, b.value)

        a.value += 1
        self.assertEqual(1, a.value)
        self.assertEqual(1, b.value)

        b.value += 1
        self.assertEqual(2, a.value)
        self.assertEqual(2, b.value)


if __name__ == "__main__":
    main()
