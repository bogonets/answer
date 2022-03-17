# -*- coding: utf-8 -*-

from unittest import TestCase, main
from argparse import Namespace
from recc.argparse.default_parser import parse_arguments_to_config
from recc.argparse.config.core_config import CoreConfig, ARG_HTTP_PORT
from recc.argparse.config.task_config import TaskConfig
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.command import Command
from recc.system.environ import exchange_env

RECC_HTTP_BIND = "RECC_HTTP_BIND"
RECC_HTTP_PORT = "RECC_HTTP_PORT"

TEST_HTTP_BIND = "1.2.3.4"
TEST_HTTP_PORT = "8888"


class DefaultParserForCoreTestCase(TestCase):
    def setUp(self):
        self.original_http_bind = exchange_env(RECC_HTTP_BIND, TEST_HTTP_BIND)
        self.original_http_port = exchange_env(RECC_HTTP_PORT, TEST_HTTP_PORT)

    def tearDown(self):
        exchange_env(RECC_HTTP_BIND, self.original_http_bind)
        exchange_env(RECC_HTTP_PORT, self.original_http_port)

    def test_parse_arguments_to_config1(self):
        config = parse_arguments_to_config(
            "-vv",
            Command.core.name,
            ARG_HTTP_PORT.long_key,
            9,
        )
        self.assertIsInstance(config, Namespace)
        self.assertIsInstance(config, GlobalConfig)
        self.assertIsInstance(config, CoreConfig)
        self.assertNotIsInstance(config, TaskConfig)
        self.assertEqual(Command.core.name, config.command)
        self.assertEqual(2, config.verbose)
        self.assertEqual(9, config.http_port)

    def test_parse_arguments_to_config2(self):
        config = parse_arguments_to_config(
            "-vv",
            Command.core.name,
            ARG_HTTP_PORT.long_key,
            9999,
            ignore_sys_argv=True,
            ignore_environment=False,
            ignore_default_paths=True,
        )
        self.assertIsInstance(config, CoreConfig)
        self.assertEqual(2, config.verbose)
        self.assertEqual(TEST_HTTP_BIND, config.http_bind)
        self.assertEqual(9999, config.http_port)


if __name__ == "__main__":
    main()
