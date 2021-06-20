# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.argument import (
    valid_key_name,
    valid_normalize_name,
    remove_start_with_dash,
)


class ArgumentTestCase(TestCase):
    def test_key_name_regex(self):
        valid_key_name("-_-01234567abYZ-_-")
        with self.assertRaises(KeyError):
            valid_key_name("a/b")
        with self.assertRaises(KeyError):
            valid_key_name("a.b")

    def test_normalize_regex(self):
        valid_normalize_name("_01234567ab_")
        with self.assertRaises(KeyError):
            valid_normalize_name("-ab-")
        with self.assertRaises(KeyError):
            valid_normalize_name("a.b")
        with self.assertRaises(KeyError):
            valid_normalize_name("ABC")

    def test_remove_start_with_dash(self):
        self.assertEqual("A", remove_start_with_dash("A"))
        self.assertEqual("A-", remove_start_with_dash("-A-"))
        self.assertEqual("help-message", remove_start_with_dash("--help-message"))

        with self.assertRaises(ValueError):
            remove_start_with_dash("")
        with self.assertRaises(ValueError):
            remove_start_with_dash("----")


if __name__ == "__main__":
    main()
