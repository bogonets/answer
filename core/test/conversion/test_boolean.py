# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.conversion.boolean import str_to_bool


class BooleanTestCase(TestCase):
    def test_str_to_bool(self):
        self.assertTrue(str_to_bool("y"))
        self.assertTrue(str_to_bool("yes"))
        self.assertTrue(str_to_bool("true"))
        self.assertTrue(str_to_bool("on"))
        self.assertTrue(str_to_bool("1"))

        self.assertFalse(str_to_bool("n"))
        self.assertFalse(str_to_bool("no"))
        self.assertFalse(str_to_bool("false"))
        self.assertFalse(str_to_bool("off"))
        self.assertFalse(str_to_bool("0"))

    def test_str_to_bool_error(self):
        with self.assertRaises(ValueError):
            self.assertFalse(str_to_bool("a"))


if __name__ == "__main__":
    main()
