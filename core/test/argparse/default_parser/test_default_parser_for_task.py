# -*- coding: utf-8 -*-

from unittest import TestCase, main
from argparse import Namespace
from recc.argparse.default_parser import parse_arguments_to_config
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.config.task_config import TaskConfig, ARG_TASK_NAME
from recc.argparse.config.global_config import GlobalConfig
from recc.argparse.command import Command


class DefaultParserForTaskTestCase(TestCase):
    def test_parse_arguments_to_config(self):
        config = parse_arguments_to_config(
            "-v",
            Command.task.name,
            ARG_TASK_NAME.long_key,
            "N",
        )
        self.assertIsInstance(config, Namespace)
        self.assertIsInstance(config, GlobalConfig)
        self.assertIsInstance(config, TaskConfig)
        self.assertNotIsInstance(config, CoreConfig)
        self.assertEqual(Command.task.name, config.command)
        self.assertEqual(1, config.verbose)
        self.assertEqual("N", config.task_name)


if __name__ == "__main__":
    main()
