# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main
from recc.argparse.parser.yaml_parse import get_namespace_by_yaml_path

TEST_HTTP_BIND = "localhost"
TEST_HTTP_PORT = 6666
TEST_VERBOSE = 7

TEST_YAML_CONTENT = f"""
recc:
    http_bind: {TEST_HTTP_BIND}
    http_port: {TEST_HTTP_PORT}
    verbose: {TEST_VERBOSE}
"""


class YamlParseTestCase(TestCase):
    def setUp(self):
        fp = tempfile.NamedTemporaryFile(delete=False)
        fp.write(TEST_YAML_CONTENT.encode("utf-8"))
        fp.close()
        self.test_yaml_path = fp.name

    def tearDown(self):
        os.unlink(self.test_yaml_path)
        self.assertFalse(os.path.exists(self.test_yaml_path))

    def test_get_namespace_by_yaml_path(self):
        config = get_namespace_by_yaml_path(self.test_yaml_path, "recc")
        self.assertEqual(TEST_HTTP_BIND, config.http_bind)
        self.assertEqual(TEST_HTTP_PORT, config.http_port)
        self.assertEqual(TEST_VERBOSE, config.verbose)


if __name__ == "__main__":
    main()
