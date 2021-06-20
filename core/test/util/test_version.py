# -*- coding: utf-8 -*-

import unittest
from recc.util.version import version_text, version_info, normalize_version


class VersionTestCase(unittest.TestCase):
    def test_version(self):
        self.assertEqual(3, len(version_text.split(".")))
        self.assertLessEqual(2, version_info[0])

    def test_normalize_version(self):
        normalize_version_info = normalize_version(version_text).split(".")
        is_extend_version_info = version_text.find("-") >= 0
        self.assertEqual(
            4 if is_extend_version_info else 3, len(normalize_version_info)
        )


if __name__ == "__main__":
    unittest.main()
