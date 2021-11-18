# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.command import Command
from recc.argparse.config.global_config import (
    GlobalConfig,
    get_global_config_and_command_args,
)


class GlobalConfigTestCase(TestCase):
    def test_empty(self):
        config, args = get_global_config_and_command_args()
        self.assertIsInstance(config, GlobalConfig)
        self.assertIsNotNone(args)
        self.assertEqual(0, len(args))

        self.assertIsNone(config.command)
        self.assertIsNone(config.config)
        self.assertFalse(config.version)
        self.assertFalse(config.help)

        self.assertIsNone(config.log_config)
        self.assertIsNone(config.log_level)

        self.assertIsNone(config.loop_driver)
        self.assertIsNone(config.json_driver)

        self.assertIsNone(config.database_host)
        self.assertIsNone(config.database_port)
        self.assertIsNone(config.database_user)
        self.assertIsNone(config.database_pw)
        self.assertIsNone(config.database_type)
        self.assertIsNone(config.database_name)

        self.assertIsNone(config.cache_host)
        self.assertIsNone(config.cache_port)
        self.assertIsNone(config.cache_pw)
        self.assertIsNone(config.cache_type)

        self.assertIsNone(config.container_host)
        self.assertIsNone(config.container_port)
        self.assertIsNone(config.container_type)

        self.assertIsNone(config.storage_type)
        self.assertIsNone(config.storage_host)
        self.assertIsNone(config.storage_port)
        self.assertIsNone(config.storage_user)
        self.assertIsNone(config.storage_pw)
        self.assertIsNone(config.storage_region)
        self.assertIsNone(config.storage_secure)

        self.assertIsNone(config.suppress_print)
        self.assertIsNone(config.verbose)
        self.assertIsNone(config.teardown)
        self.assertIsNone(config.developer)

        self.assertLess(0, len(config.help_message))
        self.assertEqual(0, len(config.unrecognized_arguments))

    def test_command_args(self):
        bind_address = "127.0.0.1"
        config, args = get_global_config_and_command_args(
            "-vv", "task", "--http-bind", bind_address
        )
        self.assertIsInstance(config, GlobalConfig)
        self.assertIsNotNone(args)
        self.assertEqual(2, len(args))
        self.assertEqual("--http-bind", args[0])
        self.assertEqual(bind_address, args[1])

        self.assertEqual(Command.task.name, config.command)
        self.assertIsNone(config.config)
        self.assertFalse(config.version)
        self.assertFalse(config.help)

        self.assertEqual(2, config.verbose)

    def test_help(self):
        config, args = get_global_config_and_command_args("-h")
        self.assertIsInstance(config, GlobalConfig)
        self.assertIsNotNone(args)
        self.assertEqual(0, len(args))
        self.assertTrue(config.help)
        self.assertLess(0, len(config.help_message))

    def test_unknown_optional_args(self):
        config, args = get_global_config_and_command_args("--unknown-optional")
        self.assertIsInstance(config, GlobalConfig)
        self.assertIsNotNone(args)
        self.assertEqual(0, len(args))
        self.assertEqual(1, len(config.unrecognized_arguments))
        self.assertEqual("--unknown-optional", config.unrecognized_arguments[0])

    # def test_unknown_positional_args(self):
    #     with self.assertRaises(ArgumentError):
    #         get_global_config_and_command_args("unknown-positional")


if __name__ == "__main__":
    main()
