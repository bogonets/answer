# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main
from tempfile import NamedTemporaryFile
from recc.argparse.parser.env_parse import (
    normalize_config_key,
    get_filtered_namespace,
    get_namespace_by_os_envs,
    get_namespace_by_os_env_files,
)
from recc.system.environ import exchange_env, get_env
from recc.variables.environment import RECC_ENV_PREFIX, RECC_ENV_FILE_SUFFIX

RECC_CONFIG = "RECC_CONFIG"
RECC_HTTP_HOST_FILE = "RECC_HTTP_HOST_FILE"
RECC_HTTP_BIND = "RECC_HTTP_BIND"
RECC_HTTP_PORT = "RECC_HTTP_PORT"
RECC_VERBOSE = "RECC_VERBOSE"
RECC_DEVELOPER = "RECC_DEVELOPER"

TEST_CONFIG = "env.conf"
TEST_HTTP_HOST = "unknown.host"
TEST_HTTP_BIND = "local"
TEST_HTTP_PORT = "8888"
TEST_VERBOSE = "2"
TEST_DEVELOPER = "true"


class EnvParseApiTestCase(TestCase):
    def test_normalize_config_key(self):
        key = "RECC_TEMP_FILE"
        self.assertEqual("temp_file", normalize_config_key(key, "RECC_"))
        self.assertEqual("recc_temp", normalize_config_key(key, None, "_FILE"))
        self.assertEqual("temp", normalize_config_key(key, "RECC_", "_FILE"))

        # Not working case:
        self.assertEqual(key.lower(), normalize_config_key(key, "ECC_"))
        self.assertEqual(key.lower(), normalize_config_key(key, "_FIL"))

        # Empty key case:
        self.assertEqual("", normalize_config_key("", "A"))
        self.assertEqual("", normalize_config_key("", None, "B"))

        # All remove case:
        self.assertEqual("", normalize_config_key(key, key))
        self.assertEqual("", normalize_config_key(key, None, key))
        self.assertEqual("", normalize_config_key(key, key, key))

    def test_get_filtered_namespace(self):
        test_dict = {
            RECC_CONFIG: "test.conf",
            RECC_HTTP_BIND: "localhost",
            RECC_HTTP_PORT: 7777,
            RECC_VERBOSE: 3,
            RECC_DEVELOPER: True,
            "CONFIG": "Unknown",
        }

        config0 = get_filtered_namespace(test_dict)
        self.assertEqual(6, len(vars(config0)))
        self.assertEqual(test_dict[RECC_CONFIG], config0.recc_config)
        self.assertEqual(test_dict[RECC_HTTP_BIND], config0.recc_http_bind)
        self.assertEqual(test_dict[RECC_HTTP_PORT], config0.recc_http_port)
        self.assertEqual(test_dict[RECC_VERBOSE], config0.recc_verbose)
        self.assertEqual(test_dict[RECC_DEVELOPER], config0.recc_developer)
        self.assertEqual("Unknown", config0.config)

        config1 = get_filtered_namespace(test_dict, "RECC_")
        self.assertEqual(5, len(vars(config1)))
        self.assertEqual(test_dict[RECC_CONFIG], config1.config)
        self.assertEqual(test_dict[RECC_HTTP_BIND], config1.http_bind)
        self.assertEqual(test_dict[RECC_HTTP_PORT], config1.http_port)
        self.assertEqual(test_dict[RECC_VERBOSE], config1.verbose)
        self.assertEqual(test_dict[RECC_DEVELOPER], config1.developer)

        config2 = get_filtered_namespace(test_dict, None, "_BIND")
        self.assertEqual(1, len(vars(config2)))
        self.assertEqual(test_dict[RECC_HTTP_BIND], config2.recc_http)

        config3 = get_filtered_namespace(test_dict, "RECC_", "_PORT")
        self.assertEqual(1, len(vars(config3)))
        self.assertEqual(test_dict[RECC_HTTP_PORT], config3.http)


class EnvParseTestCase(TestCase):
    def setUp(self):
        with NamedTemporaryFile("wt", delete=False) as f:
            self.http_host_file = f.name
            f.write(TEST_HTTP_HOST)
        self.assertTrue(os.path.isfile(self.http_host_file))

        self.original_config = exchange_env(RECC_CONFIG, TEST_CONFIG)
        self.original_http_host_file = exchange_env(
            RECC_HTTP_HOST_FILE, self.http_host_file
        )
        self.original_http_host = exchange_env(RECC_HTTP_BIND, TEST_HTTP_BIND)
        self.original_http_port = exchange_env(RECC_HTTP_PORT, TEST_HTTP_PORT)
        self.original_verbose = exchange_env(RECC_VERBOSE, TEST_VERBOSE)
        self.original_developer = exchange_env(RECC_DEVELOPER, TEST_DEVELOPER)

        self.assertEqual(TEST_CONFIG, get_env(RECC_CONFIG))
        self.assertEqual(self.http_host_file, get_env(RECC_HTTP_HOST_FILE))
        self.assertEqual(TEST_HTTP_BIND, get_env(RECC_HTTP_BIND))
        self.assertEqual(TEST_HTTP_PORT, get_env(RECC_HTTP_PORT))
        self.assertEqual(TEST_VERBOSE, get_env(RECC_VERBOSE))
        self.assertEqual(TEST_DEVELOPER, get_env(RECC_DEVELOPER))

    def tearDown(self):
        if os.path.isfile(self.http_host_file):
            os.remove(self.http_host_file)

        self.assertEqual(TEST_CONFIG, get_env(RECC_CONFIG))
        self.assertEqual(self.http_host_file, get_env(RECC_HTTP_HOST_FILE))
        self.assertEqual(TEST_HTTP_BIND, get_env(RECC_HTTP_BIND))
        self.assertEqual(TEST_HTTP_PORT, get_env(RECC_HTTP_PORT))
        self.assertEqual(TEST_VERBOSE, get_env(RECC_VERBOSE))
        self.assertEqual(TEST_DEVELOPER, get_env(RECC_DEVELOPER))

        exchange_env(RECC_CONFIG, self.original_config)
        exchange_env(RECC_HTTP_HOST_FILE, self.original_http_host_file)
        exchange_env(RECC_HTTP_BIND, self.original_http_host)
        exchange_env(RECC_HTTP_PORT, self.original_http_port)
        exchange_env(RECC_VERBOSE, self.original_verbose)
        exchange_env(RECC_DEVELOPER, self.original_developer)

    def test_get_init_params_by_os_envs(self):
        config = get_namespace_by_os_envs(RECC_ENV_PREFIX)
        self.assertEqual(TEST_HTTP_BIND, config.http_bind)
        self.assertEqual(TEST_HTTP_PORT, config.http_port)
        self.assertEqual(TEST_VERBOSE, config.verbose)
        self.assertEqual(TEST_DEVELOPER, config.developer)

    def test_get_namespace_by_os_env_files(self):
        config = get_namespace_by_os_env_files(RECC_ENV_PREFIX, RECC_ENV_FILE_SUFFIX)
        self.assertEqual(TEST_HTTP_HOST, config.http_host)


if __name__ == "__main__":
    main()
