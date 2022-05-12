# -*- coding: utf-8 -*-

import os
from argparse import Namespace
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase, main

from recc.argparse.parser.cfg_parse import get_namespace_by_cfg_path, write_cfg_file

TEST_HTTP_BIND = "localhost"
TEST_HTTP_PORT = 6666
TEST_VERBOSE = 7

TEST_CFG_CONTENT = f"""
[recc]
http_bind={TEST_HTTP_BIND}
http_port={TEST_HTTP_PORT}
verbose={TEST_VERBOSE}
"""


class CfgParseTestCase(TestCase):
    def setUp(self):
        fp = NamedTemporaryFile(delete=False)
        fp.write(TEST_CFG_CONTENT.encode("utf-8"))
        fp.close()
        self.test_cfg_path = fp.name

    def tearDown(self):
        os.unlink(self.test_cfg_path)
        self.assertFalse(os.path.exists(self.test_cfg_path))

    def test_get_namespace_by_cfg_path(self):
        config = get_namespace_by_cfg_path(self.test_cfg_path, "recc")
        self.assertEqual(TEST_HTTP_BIND, config.http_bind)
        self.assertEqual(str(TEST_HTTP_PORT), config.http_port)
        self.assertEqual(str(TEST_VERBOSE), config.verbose)


class CfgFileTestCase(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.cfg_path = os.path.join(self.temp.name, "cfg.ini")
        self.assertFalse(os.path.exists(self.cfg_path))

    def tearDown(self):
        self.temp.cleanup()

    def test_save_cfg_file(self):
        section = "recc"
        value = "value"

        namespace1 = Namespace(value=value)
        write_cfg_file(namespace1, section, self.cfg_path)
        self.assertTrue(os.path.isfile(self.cfg_path))

        namespace2 = get_namespace_by_cfg_path(self.cfg_path, section)
        self.assertEqual(namespace1.value, namespace2.value)


if __name__ == "__main__":
    main()
