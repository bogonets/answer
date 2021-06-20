# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main
from recc.argparse.parser.cfg_parse import get_namespace_by_cfg_path

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
        fp = tempfile.NamedTemporaryFile(delete=False)
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


if __name__ == "__main__":
    main()
