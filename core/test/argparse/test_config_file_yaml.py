# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main
from recc.argparse.config_file import read_config_file

TEST_YAML_CONTENT = """
recc:
    verbose: 2
    developer: true
    http_port: 80
"""


class ConfigFileYamlTestCase(TestCase):
    def setUp(self):
        fp = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False)
        fp.write(TEST_YAML_CONTENT.encode("utf-8"))
        fp.close()
        self.test_file_path = fp.name

    def tearDown(self):
        os.unlink(self.test_file_path)
        self.assertFalse(os.path.exists(self.test_file_path))

    def test_default(self):
        config = read_config_file(self.test_file_path, "recc")
        self.assertEqual(2, config.verbose)
        self.assertTrue(config.developer)
        self.assertEqual(80, config.http_port)

    def test_subsection_error(self):
        with self.assertRaises(KeyError):
            read_config_file(self.test_file_path, "recc", "kk")


if __name__ == "__main__":
    main()
