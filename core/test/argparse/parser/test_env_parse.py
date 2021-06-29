# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.parser.env_parse import (
    get_namespace_by_envs,
    get_namespace_by_os_envs,
)
from recc.system.environ import exchange_env, get_env

RECC_CONFIG = "RECC_CONFIG"
RECC_HTTP_BIND = "RECC_HTTP_BIND"
RECC_HTTP_PORT = "RECC_HTTP_PORT"
RECC_VERBOSE = "RECC_VERBOSE"

TEST_CONFIG = "env.conf"
TEST_HTTP_BIND = "local"
TEST_HTTP_PORT = "8888"
TEST_VERBOSE = "2"


class EnvParseTestCase(TestCase):
    def setUp(self):
        self.original_config = exchange_env(RECC_CONFIG, TEST_CONFIG)
        self.original_http_host = exchange_env(RECC_HTTP_BIND, TEST_HTTP_BIND)
        self.original_http_port = exchange_env(RECC_HTTP_PORT, TEST_HTTP_PORT)
        self.original_verbose = exchange_env(RECC_VERBOSE, TEST_VERBOSE)

        self.assertEqual(TEST_CONFIG, get_env(RECC_CONFIG))
        self.assertEqual(TEST_HTTP_BIND, get_env(RECC_HTTP_BIND))
        self.assertEqual(TEST_HTTP_PORT, get_env(RECC_HTTP_PORT))
        self.assertEqual(TEST_VERBOSE, get_env(RECC_VERBOSE))

    def tearDown(self):
        self.assertEqual(TEST_CONFIG, get_env(RECC_CONFIG))
        self.assertEqual(TEST_HTTP_BIND, get_env(RECC_HTTP_BIND))
        self.assertEqual(TEST_HTTP_PORT, get_env(RECC_HTTP_PORT))
        self.assertEqual(TEST_VERBOSE, get_env(RECC_VERBOSE))

        exchange_env(RECC_CONFIG, self.original_config)
        exchange_env(RECC_HTTP_BIND, self.original_http_host)
        exchange_env(RECC_HTTP_PORT, self.original_http_port)
        exchange_env(RECC_VERBOSE, self.original_verbose)

    def test_get_namespace_by_envs(self):
        test_dict = {
            RECC_CONFIG: "test.conf",
            RECC_HTTP_BIND: "localhost",
            RECC_HTTP_PORT: 7777,
            RECC_VERBOSE: 3,
        }
        config = get_namespace_by_envs(test_dict, "RECC_")
        self.assertEqual(test_dict[RECC_HTTP_BIND], config.http_bind)
        self.assertEqual(test_dict[RECC_HTTP_PORT], config.http_port)
        self.assertEqual(test_dict[RECC_VERBOSE], config.verbose)

    def test_get_init_params_by_os_envs(self):
        config = get_namespace_by_os_envs("RECC_")
        self.assertEqual(TEST_HTTP_BIND, config.http_bind)
        self.assertEqual(TEST_HTTP_PORT, config.http_port)
        self.assertEqual(TEST_VERBOSE, config.verbose)


if __name__ == "__main__":
    main()
