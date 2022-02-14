# -*- coding: utf-8 -*-

from unittest import TestCase, main
from datetime import datetime
from recc.chrono.datetime_filename import parse_dirname_and_filename


class DatetimeFilenameTestCase(TestCase):
    async def test_parse_dirname_and_filename(self):
        time = datetime(
            year=1919, month=3, day=1, hour=23, minute=9, second=1, microsecond=123456
        )
        directory, filename = parse_dirname_and_filename(time)
        self.assertEqual("1919-03-01", directory)
        self.assertEqual("23_09_01.123456", filename)


if __name__ == "__main__":
    main()
