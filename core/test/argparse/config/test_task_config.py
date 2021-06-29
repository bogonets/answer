# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.config.task_config import TaskConfig, get_task_config


class TaskConfigTestCase(TestCase):
    def test_empty(self):
        config = get_task_config()
        self.assertIsInstance(config, TaskConfig)
        self.assertFalse(config.help)
        self.assertIsNone(config.task_address)
        self.assertIsNone(config.task_register)
        self.assertIsNone(config.task_workspace_dir)
        self.assertIsNone(config.task_package_dir)
        self.assertIsNone(config.task_cache_dir)
        self.assertLess(0, len(config.help_message))
        self.assertEqual(0, len(config.unrecognized_arguments))

    def test_default(self):
        task_address = "192.168.0.2"
        config = get_task_config("--task-address", task_address)
        self.assertIsInstance(config, TaskConfig)
        self.assertEqual(task_address, config.task_address)

    def test_help(self):
        config = get_task_config("-h")
        self.assertIsInstance(config, TaskConfig)
        self.assertTrue(config.help)
        self.assertLess(0, len(config.help_message))

    def test_unknown_args(self):
        config = get_task_config("--unknown-argument")
        self.assertIsInstance(config, TaskConfig)
        self.assertEqual(1, len(config.unrecognized_arguments))
        self.assertEqual("--unknown-argument", config.unrecognized_arguments[0])


if __name__ == "__main__":
    main()
