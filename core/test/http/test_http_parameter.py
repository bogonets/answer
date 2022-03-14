# -*- coding: utf-8 -*-

from unittest import main, TestCase
from recc.http.http_parameter import cast_builtin_type_from_string


class HttpParameterTestCase(TestCase):
    def test_cast_builtin_type_from_string(self):
        self.assertIsInstance(cast_builtin_type_from_string("false", bool), bool)
        self.assertIsInstance(cast_builtin_type_from_string("1", int), int)
        self.assertIsInstance(cast_builtin_type_from_string("1.1", float), float)
        self.assertIsInstance(cast_builtin_type_from_string("k", str), str)


if __name__ == "__main__":
    main()
