# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.conversion.to_boolean import string_to_boolean


class ToBooleanTestCase(TestCase):
    def test_string_to_boolean(self):
        self.assertTrue(string_to_boolean("y"))
        self.assertTrue(string_to_boolean("yes"))
        self.assertTrue(string_to_boolean("true"))
        self.assertTrue(string_to_boolean("on"))
        self.assertTrue(string_to_boolean("1"))

        self.assertFalse(string_to_boolean("n"))
        self.assertFalse(string_to_boolean("no"))
        self.assertFalse(string_to_boolean("false"))
        self.assertFalse(string_to_boolean("off"))
        self.assertFalse(string_to_boolean("0"))

    def test_string_to_boolean_error(self):
        with self.assertRaises(ValueError):
            self.assertFalse(string_to_boolean("a"))


if __name__ == "__main__":
    main()
