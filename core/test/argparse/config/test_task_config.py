# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.config.task_config import TaskConfig, get_task_config


class TaskConfigTestCase(TestCase):
    def test_empty(self):
        config = get_task_config()
        self.assertIsInstance(config, TaskConfig)
        self.assertFalse(config.help)
        self.assertIsNone(config.task_bind)
        self.assertIsNone(config.task_port)
        self.assertIsNone(config.task_register)
        self.assertIsNone(config.task_workspace)
        self.assertLess(0, len(config.help_message))
        self.assertEqual(0, len(config.unrecognized_arguments))

    def test_default(self):
        bind_address = "192.168.0.2"
        config = get_task_config("--task-bind", bind_address)
        self.assertIsInstance(config, TaskConfig)
        self.assertEqual(bind_address, config.task_bind)

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
