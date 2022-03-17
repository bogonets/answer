# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main
from tempfile import TemporaryDirectory
from recc.argparse.default_parser import parse_arguments_to_config
from recc.argparse.config.global_config import ARG_CONFIG
from recc.argparse.config.daemon_config import DaemonConfig, ARG_DAEMON_SCRIPT
from recc.argparse.command import Command
from recc.system.environ import exchange_env
from recc.variables.argparse import RECC_DOM_ROOT

RECC_VERBOSE = "RECC_VERBOSE"
RECC_CONFIG = "RECC_CONFIG"
RECC_DATABASE_PW_FILE = "RECC_DATABASE_PW_FILE"
RECC_DEVELOPER = "RECC_DEVELOPER"
RECC_DAEMON_ADDRESS = "RECC_DAEMON_ADDRESS"
RECC_DAEMON_SCRIPT = "RECC_DAEMON_SCRIPT"
RECC_DAEMON_PACKAGES_DIR = "RECC_DAEMON_PACKAGES_DIR"

CONFIG_SCRIPT0 = "/config/script/file/0"
CONFIG_SCRIPT1 = "/config/script/file/1"
CONFIG_SCRIPT2 = "/config/script/file/2"
CONFIG_SCRIPT3 = "/config/script/file/3"
CONFIG_PACKAGES_DIR0 = "/config/package/dir/0"
CONFIG_PACKAGES_DIR1 = "/config/package/dir/1"
CONFIG_PACKAGES_DIR2 = "/config/package/dir/2"
CONFIG_PACKAGES_DIR3 = "/config/package/dir/3"
CONFIG_PACKAGES_DIR4 = "/config/package/dir/4"
CONFIG_PACKAGES_DIR5 = "/config/package/dir/5"
CONFIG_PACKAGES_DIR6 = "/config/package/dir/6"
CONFIG_PACKAGES_DIR7 = "/config/package/dir/7"

TEST_VERBOSE = "3"
TEST_DEVELOPER = "True"
TEST_DAEMON_ADDRESS = "localhost:9999"
TEST_DAEMON_SCRIPT = CONFIG_SCRIPT0
TEST_DAEMON_PACKAGES_DIR = f"{CONFIG_PACKAGES_DIR0}:{CONFIG_PACKAGES_DIR1}"

CONFIG_CFG = f"""
[{RECC_DOM_ROOT}]
verbose=10
daemon_script={CONFIG_SCRIPT1}
daemon_packages_dir={CONFIG_PACKAGES_DIR2}:{CONFIG_PACKAGES_DIR3}
"""

CONFIG_JSON0 = f"""
{{
    "{RECC_DOM_ROOT}": {{
        "verbose": 20,
        "daemon_script": "{CONFIG_SCRIPT2}",
        "daemon_packages_dir": ["{CONFIG_PACKAGES_DIR4}", "{CONFIG_PACKAGES_DIR5}"]
    }}
}}
"""

CONFIG_JSON1 = f"""
{{
    "{RECC_DOM_ROOT}": {{
        "verbose": 30,
        "daemon_script": "{CONFIG_SCRIPT2}",
        "daemon_packages_dir": "{CONFIG_PACKAGES_DIR4}:{CONFIG_PACKAGES_DIR5}"
    }}
}}
"""

CONFIG_YAML0 = f"""
{RECC_DOM_ROOT}:
    verbose: 40
    daemon_script: {CONFIG_SCRIPT3}
    daemon_packages_dir:
        - {CONFIG_PACKAGES_DIR6}
        - {CONFIG_PACKAGES_DIR7}
"""

CONFIG_YAML1 = f"""
{RECC_DOM_ROOT}:
    verbose: 50
    daemon_script: {CONFIG_SCRIPT3}
    daemon_packages_dir: "{CONFIG_PACKAGES_DIR6}:{CONFIG_PACKAGES_DIR7}"
"""


class DefaultParserForDaemonTestCase(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.config_cfg_path = os.path.join(self.temp.name, "config.cfg")
        self.config_json0_path = os.path.join(self.temp.name, "config0.json")
        self.config_json1_path = os.path.join(self.temp.name, "config1.json")
        self.config_yaml0_path = os.path.join(self.temp.name, "config0.yaml")
        self.config_yaml1_path = os.path.join(self.temp.name, "config1.yaml")
        self.database_pw_file_path = os.path.join(self.temp.name, "db.pw")
        self.database_pw = "1234"

        with open(self.config_cfg_path, "w") as f:
            f.write(CONFIG_CFG)
        with open(self.config_json0_path, "w") as f:
            f.write(CONFIG_JSON0)
        with open(self.config_json1_path, "w") as f:
            f.write(CONFIG_JSON1)
        with open(self.config_yaml0_path, "w") as f:
            f.write(CONFIG_YAML0)
        with open(self.config_yaml1_path, "w") as f:
            f.write(CONFIG_YAML1)
        with open(self.database_pw_file_path, "w") as f:
            f.write(self.database_pw)

        self.assertTrue(os.path.isfile(self.config_cfg_path))
        self.assertTrue(os.path.isfile(self.config_json0_path))
        self.assertTrue(os.path.isfile(self.config_json1_path))
        self.assertTrue(os.path.isfile(self.config_yaml0_path))
        self.assertTrue(os.path.isfile(self.config_yaml1_path))
        self.assertTrue(os.path.isfile(self.database_pw_file_path))

        self.original_verbose = exchange_env(RECC_VERBOSE, TEST_VERBOSE)
        self.original_config = exchange_env(RECC_CONFIG, self.config_cfg_path)
        self.original_database_pw_file = exchange_env(
            RECC_DATABASE_PW_FILE, self.database_pw_file_path
        )
        self.original_developer = exchange_env(RECC_DEVELOPER, TEST_DEVELOPER)
        self.original_daemon_address = exchange_env(
            RECC_DAEMON_ADDRESS, TEST_DAEMON_ADDRESS
        )
        self.original_daemon_file = exchange_env(RECC_DAEMON_SCRIPT, TEST_DAEMON_SCRIPT)
        self.original_daemon_packages_dir = exchange_env(
            RECC_DAEMON_PACKAGES_DIR, TEST_DAEMON_PACKAGES_DIR
        )

    def tearDown(self):
        exchange_env(RECC_VERBOSE, self.original_verbose)
        exchange_env(RECC_CONFIG, self.original_config)
        exchange_env(RECC_DATABASE_PW_FILE, self.original_database_pw_file)
        exchange_env(RECC_DEVELOPER, self.original_developer)
        exchange_env(RECC_DAEMON_ADDRESS, self.original_daemon_address)
        exchange_env(RECC_DAEMON_SCRIPT, self.original_daemon_file)
        exchange_env(RECC_DAEMON_PACKAGES_DIR, self.original_daemon_packages_dir)
        self.temp.cleanup()

    def test_parse_arguments_to_config(self):
        daemon_script = "/unknown/path"
        config = parse_arguments_to_config(
            Command.daemon.name,
            ARG_DAEMON_SCRIPT.long_key,
            daemon_script,
            ignore_sys_argv=True,
            ignore_environment=False,
            ignore_default_paths=True,
        )
        self.assertIsInstance(config, DaemonConfig)
        self.assertEqual(10, config.verbose)
        self.assertEqual(self.config_cfg_path, config.config)
        self.assertEqual(self.database_pw, config.database_pw)
        self.assertTrue(config.developer)

        self.assertEqual(TEST_DAEMON_ADDRESS, config.daemon_address)
        self.assertEqual(daemon_script, config.daemon_script)
        self.assertIsInstance(config.daemon_packages_dir, list)
        self.assertEqual(2, len(config.daemon_packages_dir))
        self.assertEqual(CONFIG_PACKAGES_DIR2, config.daemon_packages_dir[0])
        self.assertEqual(CONFIG_PACKAGES_DIR3, config.daemon_packages_dir[1])

    def test_parse_arguments_to_config_json0(self):
        daemon_script = "/unknown/path"
        config = parse_arguments_to_config(
            ARG_CONFIG.long_key,
            self.config_json0_path,
            Command.daemon.name,
            ARG_DAEMON_SCRIPT.long_key,
            daemon_script,
            ignore_sys_argv=True,
            ignore_environment=False,
            ignore_default_paths=True,
        )
        self.assertIsInstance(config, DaemonConfig)
        self.assertEqual(20, config.verbose)
        self.assertEqual(self.config_json0_path, config.config)
        self.assertEqual(self.database_pw, config.database_pw)
        self.assertTrue(config.developer)

        self.assertEqual(TEST_DAEMON_ADDRESS, config.daemon_address)
        self.assertEqual(daemon_script, config.daemon_script)
        self.assertIsInstance(config.daemon_packages_dir, list)
        self.assertEqual(2, len(config.daemon_packages_dir))
        self.assertEqual(CONFIG_PACKAGES_DIR4, config.daemon_packages_dir[0])
        self.assertEqual(CONFIG_PACKAGES_DIR5, config.daemon_packages_dir[1])

    def test_parse_arguments_to_config_json1(self):
        daemon_script = "/unknown/path"
        config = parse_arguments_to_config(
            ARG_CONFIG.long_key,
            self.config_json1_path,
            Command.daemon.name,
            ARG_DAEMON_SCRIPT.long_key,
            daemon_script,
            ignore_sys_argv=True,
            ignore_environment=False,
            ignore_default_paths=True,
        )
        self.assertIsInstance(config, DaemonConfig)
        self.assertEqual(30, config.verbose)
        self.assertEqual(self.config_json1_path, config.config)
        self.assertEqual(self.database_pw, config.database_pw)
        self.assertTrue(config.developer)

        self.assertEqual(TEST_DAEMON_ADDRESS, config.daemon_address)
        self.assertEqual(daemon_script, config.daemon_script)
        self.assertIsInstance(config.daemon_packages_dir, list)
        self.assertEqual(2, len(config.daemon_packages_dir))
        self.assertEqual(CONFIG_PACKAGES_DIR4, config.daemon_packages_dir[0])
        self.assertEqual(CONFIG_PACKAGES_DIR5, config.daemon_packages_dir[1])

    def test_parse_arguments_to_config_yaml0(self):
        daemon_script = "/unknown/path"
        config = parse_arguments_to_config(
            ARG_CONFIG.long_key,
            self.config_yaml0_path,
            Command.daemon.name,
            ARG_DAEMON_SCRIPT.long_key,
            daemon_script,
            ignore_sys_argv=True,
            ignore_environment=False,
            ignore_default_paths=True,
        )
        self.assertIsInstance(config, DaemonConfig)
        self.assertEqual(40, config.verbose)
        self.assertEqual(self.config_yaml0_path, config.config)
        self.assertEqual(self.database_pw, config.database_pw)
        self.assertTrue(config.developer)

        self.assertEqual(TEST_DAEMON_ADDRESS, config.daemon_address)
        self.assertEqual(daemon_script, config.daemon_script)
        self.assertIsInstance(config.daemon_packages_dir, list)
        self.assertEqual(2, len(config.daemon_packages_dir))
        self.assertEqual(CONFIG_PACKAGES_DIR6, config.daemon_packages_dir[0])
        self.assertEqual(CONFIG_PACKAGES_DIR7, config.daemon_packages_dir[1])

    def test_parse_arguments_to_config_yaml1(self):
        daemon_script = "/unknown/path"
        config = parse_arguments_to_config(
            ARG_CONFIG.long_key,
            self.config_yaml1_path,
            Command.daemon.name,
            ARG_DAEMON_SCRIPT.long_key,
            daemon_script,
            ignore_sys_argv=True,
            ignore_environment=False,
            ignore_default_paths=True,
        )
        self.assertIsInstance(config, DaemonConfig)
        self.assertEqual(50, config.verbose)
        self.assertEqual(self.config_yaml1_path, config.config)
        self.assertEqual(self.database_pw, config.database_pw)
        self.assertTrue(config.developer)

        self.assertEqual(TEST_DAEMON_ADDRESS, config.daemon_address)
        self.assertEqual(daemon_script, config.daemon_script)
        self.assertIsInstance(config.daemon_packages_dir, list)
        self.assertEqual(2, len(config.daemon_packages_dir))
        self.assertEqual(CONFIG_PACKAGES_DIR6, config.daemon_packages_dir[0])
        self.assertEqual(CONFIG_PACKAGES_DIR7, config.daemon_packages_dir[1])


if __name__ == "__main__":
    main()
