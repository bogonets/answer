# -*- coding: utf-8 -*-

import unittest
from functools import reduce
from recc.__main__ import main as root_main
from recc.util.version import version_text


class VersionTestCase(unittest.TestCase):
    def setUp(self):
        self.print_buffer = str()

    def tearDown(self):
        pass

    def _printer(self, *args) -> None:
        self.print_buffer += reduce(lambda x, y: x + y, *args)

    def test_root_main(self):
        self.assertEqual(0, root_main(["--version"], printer=self._printer))
        self.assertEqual(version_text, self.print_buffer)


if __name__ == "__main__":
    unittest.main()
