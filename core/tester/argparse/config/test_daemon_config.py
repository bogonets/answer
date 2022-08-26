# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.argparse.argument_parser import ArgumentMessage
from recc.argparse.command import Command
from recc.argparse.config.daemon_config import (
    ARG_DAEMON_ADDRESS,
    ARG_DAEMON_MODULE,
    ARG_DAEMON_PACKAGES_DIR,
    DaemonConfig,
)
from recc.argparse.default_parser import parse_arguments_to_config


class DaemonConfigTestCase(TestCase):
    def test_empty(self):
        config = parse_arguments_to_config(Command.daemon.name)
        self.assertIsInstance(config, DaemonConfig)
        self.assertEqual(config.command, Command.daemon.name)
        self.assertIsNotNone(config.daemon_address)
        self.assertIsNotNone(config.daemon_module)
        self.assertIsNotNone(config.daemon_packages_dir)

    def test_config(self):
        address = "192.168.0.1"
        file = "/script/path/python"
        package1 = "/package/dir/1"
        package2 = "/package/dir/2"
        config = parse_arguments_to_config(
            Command.daemon.name,
            ARG_DAEMON_ADDRESS.long_key,
            address,
            ARG_DAEMON_MODULE.long_key,
            file,
            ARG_DAEMON_PACKAGES_DIR.long_key,
            package1,
            ARG_DAEMON_PACKAGES_DIR.long_key,
            package2,
        )
        self.assertIsInstance(config, DaemonConfig)
        self.assertEqual(config.command, Command.daemon.name)
        self.assertEqual(address, config.daemon_address)
        self.assertEqual(file, config.daemon_module)
        self.assertEqual(2, len(config.daemon_packages_dir))
        self.assertEqual(package1, config.daemon_packages_dir[0])
        self.assertEqual(package2, config.daemon_packages_dir[1])

    def test_unknown_args(self):
        with self.assertRaises(ArgumentMessage):
            parse_arguments_to_config(Command.daemon.name, "--unknown-argument")


if __name__ == "__main__":
    main()
