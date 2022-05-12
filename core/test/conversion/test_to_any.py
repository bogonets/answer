# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.conversion.to_any import string_to_any


class ToAnyTestCase(TestCase):
    def test_cast_builtin_type_from_string(self):
        self.assertIsInstance(string_to_any("false", bool), bool)
        self.assertIsInstance(string_to_any("1", int), int)
        self.assertIsInstance(string_to_any("1.1", float), float)
        self.assertIsInstance(string_to_any("k", str), str)


if __name__ == "__main__":
    main()
