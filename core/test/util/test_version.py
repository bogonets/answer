# -*- coding: utf-8 -*-

import unittest

from recc.util.version import (
    normalize_version,
    parse_version_numbers,
    version_text,
    version_tuple,
)


class VersionTestCase(unittest.TestCase):
    def test_version(self):
        self.assertEqual(3, len(version_text.split(".")))
        self.assertLessEqual(2, version_tuple[0])

    def test_parse_semantic_version(self):
        self.assertTupleEqual((1, 2, 3), parse_version_numbers("1.2.3-dev10"))
        self.assertTupleEqual((0, 0, 0), parse_version_numbers("0.0.0"))
        self.assertTupleEqual((90, 2, 20), parse_version_numbers("90.02.20"))

    def test_normalize_version(self):
        normalize_version_info = normalize_version(version_text).split(".")
        is_extend_version_info = version_text.find("-") >= 0
        self.assertEqual(
            4 if is_extend_version_info else 3, len(normalize_version_info)
        )


if __name__ == "__main__":
    unittest.main()
