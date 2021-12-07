# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.argument_parser import ArgumentMessage
from recc.argparse.config.task_config import TaskConfig
from recc.argparse.default_parser import parse_arguments_to_config
from recc.argparse.command import Command


class TaskConfigTestCase(TestCase):
    def test_empty(self):
        config = parse_arguments_to_config(Command.task.name)
        self.assertIsInstance(config, TaskConfig)
        self.assertEqual(config.command, Command.task.name)
        self.assertIsNotNone(config.task_address)
        self.assertIsNotNone(config.task_register)
        self.assertIsNotNone(config.task_group)
        self.assertIsNotNone(config.task_project)
        self.assertIsNotNone(config.task_name)
        self.assertIsNotNone(config.task_workspace_dir)
        self.assertIsNotNone(config.task_package_dir)
        self.assertIsNotNone(config.task_cache_dir)

    def test_default(self):
        task_address = "192.168.0.2"
        config = parse_arguments_to_config(
            Command.task.name, "--task-address", task_address
        )
        self.assertIsInstance(config, TaskConfig)
        self.assertEqual(config.command, Command.task.name)
        self.assertEqual(task_address, config.task_address)

    def test_unknown_args(self):
        with self.assertRaises(ArgumentMessage):
            parse_arguments_to_config(Command.task.name, "--unknown-argument")


if __name__ == "__main__":
    main()
