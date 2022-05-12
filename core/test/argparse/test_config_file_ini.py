# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main

from recc.argparse.config_file import read_config_file

TEST_FLAG_VALUE = "Hello, World!"
TEST_INI_CONTENT = f"""
[recc]
flag={TEST_FLAG_VALUE}
"""


class ConfigFileIniTestCase(TestCase):
    def setUp(self):
        fp = tempfile.NamedTemporaryFile(suffix=".ini", delete=False)
        fp.write(TEST_INI_CONTENT.encode("utf-8"))
        fp.close()
        self.test_file_path = fp.name

    def tearDown(self):
        os.unlink(self.test_file_path)
        self.assertFalse(os.path.exists(self.test_file_path))

    def test_default(self):
        config = read_config_file(self.test_file_path, "recc")
        self.assertEqual(TEST_FLAG_VALUE, config.flag)

    def test_subsection_error(self):
        with self.assertRaises(IndexError):
            read_config_file(self.test_file_path, "recc", "kk")


if __name__ == "__main__":
    main()
