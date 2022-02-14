# -*- coding: utf-8 -*-

from unittest import TestCase, main
from datetime import date
from recc.chrono.date_parse import parse_yyyy_mm_dd


class DateParseTestCase(TestCase):
    def test_parse_yyyy_mm_dd(self):
        self.assertEqual(date(2000, 10, 22), parse_yyyy_mm_dd("2000-10-22"))
        self.assertEqual(date(1990, 1, 1), parse_yyyy_mm_dd("1990-01-01"))


if __name__ == "__main__":
    main()
