# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.default_parser import parse_arguments_to_config
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.config.task_config import TaskConfig
from recc.argparse.command import Command
from recc.system.environ import exchange_env

RECC_VERBOSE = "RECC_VERBOSE"
RECC_DEVELOPER = "RECC_DEVELOPER"


class DefaultParserForGlobalTestCase(TestCase):
    def setUp(self):
        self.original_verbose = exchange_env(RECC_VERBOSE, "100")
        self.original_developer = exchange_env(RECC_DEVELOPER, "True")

    def tearDown(self):
        exchange_env(RECC_VERBOSE, self.original_verbose)
        exchange_env(RECC_DEVELOPER, self.original_developer)

    def test_parse_arguments_to_config(self):
        config1 = parse_arguments_to_config(
            Command.core.name,
            ignore_sys_argv=True,
            ignore_environment=False,
            ignore_default_paths=True,
        )
        self.assertIsInstance(config1, CoreConfig)
        self.assertEqual(100, config1.verbose)
        self.assertTrue(config1.developer)

        config2 = parse_arguments_to_config(
            "-vv",
            Command.task.name,
            ignore_sys_argv=True,
            ignore_environment=False,
            ignore_default_paths=True,
        )
        self.assertIsInstance(config2, TaskConfig)
        self.assertEqual(2, config2.verbose)
        self.assertTrue(config2.developer)


if __name__ == "__main__":
    main()
