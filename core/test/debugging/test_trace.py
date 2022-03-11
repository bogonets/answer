# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.debugging.trace import is_debugging_mode


class TraceTestCase(TestCase):
    def test_default(self):
        self.assertIsInstance(is_debugging_mode(), bool)


if __name__ == "__main__":
    main()
