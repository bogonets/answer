# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.config.core_config import CoreConfig, get_core_config


class CoreConfigTestCase(TestCase):
    def test_empty(self):
        config = get_core_config()
        self.assertIsInstance(config, CoreConfig)
        self.assertFalse(config.help)
        self.assertIsNone(config.external_host)
        self.assertIsNone(config.http_bind)
        self.assertIsNone(config.http_port)
        self.assertIsNone(config.http_root)
        self.assertIsNone(config.http_timeout)
        self.assertIsNone(config.manage_port_min)
        self.assertIsNone(config.manage_port_max)
        self.assertIsNone(config.storage_root)
        self.assertIsNone(config.signature)
        self.assertLess(0, len(config.help_message))
        self.assertEqual(0, len(config.unrecognized_arguments))

    def test_default(self):
        bind_address = "192.168.0.1"
        config = get_core_config("--http-bind", bind_address)
        self.assertIsInstance(config, CoreConfig)
        self.assertEqual(bind_address, config.http_bind)

    def test_help(self):
        config = get_core_config("-h")
        self.assertIsInstance(config, CoreConfig)
        self.assertTrue(config.help)
        self.assertLess(0, len(config.help_message))

    def test_unknown_args(self):
        config = get_core_config("--unknown-argument")
        self.assertIsInstance(config, CoreConfig)
        self.assertEqual(1, len(config.unrecognized_arguments))
        self.assertEqual("--unknown-argument", config.unrecognized_arguments[0])


if __name__ == "__main__":
    main()
