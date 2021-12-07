# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.argument_parser import ArgumentMessage
from recc.argparse.config.core_config import CoreConfig
from recc.argparse.default_parser import parse_arguments_to_config
from recc.argparse.command import Command


class CoreConfigTestCase(TestCase):
    def test_empty(self):
        config = parse_arguments_to_config(Command.core.name)
        self.assertIsInstance(config, CoreConfig)
        self.assertEqual(config.command, Command.core.name)
        self.assertIsNotNone(config.external_host)
        self.assertIsNotNone(config.http_bind)
        self.assertIsNotNone(config.http_port)
        self.assertIsNotNone(config.http_root)
        self.assertIsNotNone(config.http_timeout)
        self.assertIsNotNone(config.manage_port_min)
        self.assertIsNotNone(config.manage_port_max)
        self.assertIsNotNone(config.storage_root)
        self.assertIsNotNone(config.signature)
        self.assertIsNotNone(config.public_signup)
        self.assertIsNotNone(config.access_token_duration)
        self.assertIsNotNone(config.refresh_token_duration)

    def test_default(self):
        bind_address = "192.168.0.1"
        config = parse_arguments_to_config(
            Command.core.name, "--http-bind", bind_address
        )
        self.assertIsInstance(config, CoreConfig)
        self.assertEqual(config.command, Command.core.name)
        self.assertEqual(bind_address, config.http_bind)

    def test_config(self):
        config_path = "/usr/local/recc/home/config.yml"
        http_bind = "192.168.0.1"
        http_port = 300
        config = parse_arguments_to_config(
            "--config",
            config_path,
            Command.core.name,
            "--http-bind",
            http_bind,
            "--http-port",
            http_port,
        )
        self.assertIsInstance(config, CoreConfig)
        self.assertEqual(config.command, Command.core.name)
        self.assertEqual(config_path, config.config)
        self.assertEqual(http_bind, config.http_bind)
        self.assertEqual(http_port, config.http_port)

    def test_unknown_args(self):
        with self.assertRaises(ArgumentMessage):
            parse_arguments_to_config(Command.core.name, "--unknown-argument")


if __name__ == "__main__":
    main()
