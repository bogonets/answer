# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main
from recc.argparse.parser.json_parse import get_namespace_by_json_path

TEST_HTTP_BIND = "localhost"
TEST_HTTP_PORT = 6666
TEST_VERBOSE = 7

TEST_JSON_BODY = f"""{{
    "recc": {{
        "http_bind": "{TEST_HTTP_BIND}",
        "http_port": {TEST_HTTP_PORT},
        "verbose": {TEST_VERBOSE},
        "daemon_packages_dir": [
            "/package/dir/1",
            "/package/dir/2"
        ]
    }}
}}"""


class JsonParseTestCase(TestCase):
    def setUp(self):
        fp = tempfile.NamedTemporaryFile(delete=False)
        fp.write(TEST_JSON_BODY.encode("utf-8"))
        fp.close()
        self.test_json_path = fp.name

    def tearDown(self):
        os.unlink(self.test_json_path)
        self.assertFalse(os.path.exists(self.test_json_path))

    def test_get_namespace_by_json_path(self):
        config = get_namespace_by_json_path(self.test_json_path, "recc")
        self.assertEqual(TEST_HTTP_BIND, config.http_bind)
        self.assertEqual(TEST_HTTP_PORT, config.http_port)
        self.assertEqual(TEST_VERBOSE, config.verbose)

        self.assertIsInstance(config.daemon_packages_dir, list)
        self.assertEqual(2, len(config.daemon_packages_dir))
        self.assertEqual("/package/dir/1", config.daemon_packages_dir[0])
        self.assertEqual("/package/dir/2", config.daemon_packages_dir[1])


if __name__ == "__main__":
    main()
