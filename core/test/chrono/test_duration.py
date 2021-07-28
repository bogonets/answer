# -*- coding: utf-8 -*-

from unittest import TestCase, main
from datetime import timedelta
from recc.chrono.duration import duration_to_timedelta


class DurationTestCase(TestCase):
    def test_duration_to_timedelta(self):
        self.assertEqual(timedelta(seconds=0.1), duration_to_timedelta("0.1 s"))
        self.assertEqual(timedelta(seconds=0.2), duration_to_timedelta("0.2 sec"))
        self.assertEqual(timedelta(seconds=0.3), duration_to_timedelta("0.3 second"))
        self.assertEqual(timedelta(seconds=0.4), duration_to_timedelta("0.4 seconds"))

        self.assertEqual(timedelta(minutes=1), duration_to_timedelta("1.m"))
        self.assertEqual(timedelta(minutes=2), duration_to_timedelta("2.min"))
        self.assertEqual(timedelta(minutes=3), duration_to_timedelta("3.minute"))
        self.assertEqual(timedelta(minutes=4), duration_to_timedelta("4.minutes"))

        self.assertEqual(timedelta(hours=1), duration_to_timedelta("1h"))
        self.assertEqual(timedelta(hours=2), duration_to_timedelta("2hour"))
        self.assertEqual(timedelta(hours=3), duration_to_timedelta("3hours"))

        self.assertEqual(timedelta(days=0.1), duration_to_timedelta("0.1d"))
        self.assertEqual(timedelta(days=0.2), duration_to_timedelta("0.2day"))
        self.assertEqual(timedelta(days=0.3), duration_to_timedelta("0.3days"))

        self.assertEqual(timedelta(weeks=0.1), duration_to_timedelta("0.1w"))
        self.assertEqual(timedelta(weeks=0.2), duration_to_timedelta("0.2week"))
        self.assertEqual(timedelta(weeks=0.3), duration_to_timedelta("0.3weeks"))

    def test_0_duration_to_timedelta(self):
        self.assertEqual(timedelta(seconds=0), duration_to_timedelta("0.0s"))
        self.assertEqual(timedelta(seconds=0), duration_to_timedelta("0.s"))
        self.assertEqual(timedelta(seconds=0), duration_to_timedelta("0s"))

        self.assertEqual(timedelta(weeks=0), duration_to_timedelta("0w"))
        self.assertEqual(timedelta(days=0), duration_to_timedelta("0d"))
        self.assertEqual(timedelta(hours=0), duration_to_timedelta("0h"))
        self.assertEqual(timedelta(minutes=0), duration_to_timedelta("0m"))
        self.assertEqual(timedelta(seconds=0), duration_to_timedelta("0s"))
        self.assertEqual(timedelta(microseconds=0), duration_to_timedelta("0micro"))
        self.assertEqual(timedelta(milliseconds=0), duration_to_timedelta("0milli"))

    def test_duration_to_timedelta_errors(self):
        with self.assertRaises(ValueError):
            duration_to_timedelta("0.6")
        with self.assertRaises(ValueError):
            duration_to_timedelta("2.")
        with self.assertRaises(ValueError):
            duration_to_timedelta("0")
        with self.assertRaises(ValueError):
            duration_to_timedelta("")
        with self.assertRaises(ValueError):
            duration_to_timedelta(" s")
        with self.assertRaises(ValueError):
            duration_to_timedelta("s")


if __name__ == "__main__":
    main()
