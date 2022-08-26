# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.regex.access_filter import access_filter


class AccessFilterTestCase(TestCase):
    def test_access_filter(self):
        self.assertListEqual(["1", "2", "3"], access_filter(["1", "2", "3"]))
        self.assertListEqual(
            ["123", "345"],
            access_filter(["123", "234", "345"], denies=[r".*4$"]),
        )
        self.assertListEqual(
            ["123", "234"],
            access_filter(["123", "234", "345"], allows=[r".*2.*"]),
        )
        self.assertListEqual(
            ["123"],
            access_filter(["123", "234", "345"], denies=[r".*4$"], allows=[r".*2.*"]),
        )


if __name__ == "__main__":
    main()
