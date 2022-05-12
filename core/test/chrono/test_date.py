# -*- coding: utf-8 -*-

from datetime import date, datetime
from unittest import TestCase, main

from recc.chrono.date import date_to_datetime_range, parse_yyyy_mm_dd


class DateParseTestCase(TestCase):
    def test_parse_yyyy_mm_dd(self):
        self.assertEqual(date(2000, 10, 22), parse_yyyy_mm_dd("2000-10-22"))
        self.assertEqual(date(1990, 1, 1), parse_yyyy_mm_dd("1990-01-01"))

    def test_date_to_datetime_range(self):
        left, right = date_to_datetime_range(date(1990, 1, 1))
        self.assertEqual(left, datetime(1990, 1, 1, 0, 0, 0, 0))
        self.assertEqual(right, datetime(1990, 1, 1, 23, 59, 59, 999999))


if __name__ == "__main__":
    main()
