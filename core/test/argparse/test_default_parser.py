# -*- coding: utf-8 -*-

from unittest import TestCase, main
from argparse import Namespace
from recc.argparse.default_parser import (
    ConfigType,
    left_join,
    parse_arguments_to_config,
)
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.config.task_config import TaskConfig
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.command import Command
from recc.system.environ import exchange_env

RECC_HTTP_BIND = "RECC_HTTP_BIND"
RECC_HTTP_PORT = "RECC_HTTP_PORT"
RECC_VERBOSE = "RECC_VERBOSE"
RECC_DEVELOPER = "RECC_DEVELOPER"


def _parse_arguments_to_config(*args) -> ConfigType:
    return parse_arguments_to_config(
        *args,
        ignore_sys_argv=True,
        ignore_environment=False,
        ignore_default_paths=True,
    )


class DefaultParserTestCase(TestCase):
    def test_left_join_for_empty_object(self):
        name1 = Namespace(a=1, b=2)
        name2 = Namespace(c=3, d=4)

        result = Namespace()
        left_join(result, Namespace(), name1, None, name2, None, Namespace())
        self.assertEqual(4, len(vars(result)))
        self.assertEqual(1, result.a)
        self.assertEqual(2, result.b)
        self.assertEqual(3, result.c)
        self.assertEqual(4, result.d)

    def test_left_join_for_normal(self):
        name1 = Namespace(a=1, b=2)
        name2 = Namespace(c=3, d=4)
        name3 = Namespace(a=5, c=6)

        result = Namespace()
        left_join(result, name1, name2, name3)
        self.assertEqual(4, len(vars(result)))
        self.assertEqual(1, result.a)
        self.assertEqual(2, result.b)
        self.assertEqual(3, result.c)
        self.assertEqual(4, result.d)

    def test_left_join_for_none_merge(self):
        name1 = Namespace(a=None, b=2, c=3)
        name2 = Namespace(a=1, b=None, c=4)

        result = Namespace()
        left_join(result, name1, name2)
        self.assertEqual(3, len(vars(result)))
        self.assertEqual(1, result.a)
        self.assertEqual(2, result.b)
        self.assertEqual(3, result.c)

    def test_parse_arguments_to_config_for_core(self):
        config = parse_arguments_to_config("-vv", Command.core.name, "--http-port", 9)
        self.assertIsInstance(config, Namespace)
        self.assertIsInstance(config, GlobalConfig)
        self.assertIsInstance(config, CoreConfig)
        self.assertNotIsInstance(config, TaskConfig)
        self.assertEqual(Command.core.name, config.command)
        self.assertEqual(2, config.verbose)
        self.assertEqual(9, config.http_port)

    def test_parse_arguments_to_config_for_task(self):
        config = parse_arguments_to_config("-v", Command.task.name, "--task-name", "N")
        self.assertIsInstance(config, Namespace)
        self.assertIsInstance(config, GlobalConfig)
        self.assertIsInstance(config, TaskConfig)
        self.assertNotIsInstance(config, CoreConfig)
        self.assertEqual(Command.task.name, config.command)
        self.assertEqual(1, config.verbose)
        self.assertEqual("N", config.task_name)

    def test_parse_arguments_to_global_config(self):
        original_verbose = exchange_env(RECC_VERBOSE, "100")
        original_developer = exchange_env(RECC_DEVELOPER, "True")

        config1 = _parse_arguments_to_config("core")
        self.assertIsInstance(config1, CoreConfig)
        self.assertEqual(100, config1.verbose)
        self.assertTrue(config1.developer)

        config2 = _parse_arguments_to_config("-vv", "task")
        self.assertIsInstance(config2, TaskConfig)
        self.assertEqual(2, config2.verbose)
        self.assertTrue(config2.developer)

        exchange_env(RECC_VERBOSE, original_verbose)
        exchange_env(RECC_DEVELOPER, original_developer)

    def test_parse_arguments_to_core_config(self):
        original_http_bind = exchange_env(RECC_HTTP_BIND, "1.2.3.4")
        original_http_port = exchange_env(RECC_HTTP_PORT, "8888")

        config = _parse_arguments_to_config("-vv", "core", "--http-port", 9999)
        self.assertIsInstance(config, CoreConfig)
        self.assertEqual(2, config.verbose)
        self.assertEqual("1.2.3.4", config.http_bind)
        self.assertEqual(9999, config.http_port)

        exchange_env(RECC_HTTP_BIND, original_http_bind)
        exchange_env(RECC_HTTP_PORT, original_http_port)


if __name__ == "__main__":
    main()
