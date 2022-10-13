# -*- coding: utf-8 -*-

from argparse import Namespace
from unittest import TestCase, main

from recc.arguments import default_argument_parser


class ArgumentsTestCase(TestCase):
    def test_empty_arguments(self):
        parser = default_argument_parser()
        args = parser.parse_known_args([])[0]

        # Do not use for loops.
        # It also tests whether the arguments used are correct.
        self.assertIsNotNone(args)
        self.assertIsInstance(args, Namespace)

        self.assertIsNone(args.http_bind)
        self.assertIsNone(args.http_port)
        self.assertIsNone(args.http_root)
        self.assertIsNone(args.http_timeout)
        self.assertIsNone(args.database_host)
        self.assertIsNone(args.database_port)
        self.assertIsNone(args.database_user)
        self.assertIsNone(args.database_pw)
        self.assertIsNone(args.database_name)
        self.assertIsNone(args.database_timeout)
        self.assertIsNone(args.cache_host)
        self.assertIsNone(args.cache_port)
        self.assertIsNone(args.cache_secret)
        self.assertIsNone(args.cache_prefix)
        self.assertIsNone(args.cache_timeout)
        self.assertIsNone(args.storage_host)
        self.assertIsNone(args.storage_port)
        self.assertIsNone(args.storage_access)
        self.assertIsNone(args.storage_secret)
        self.assertIsNone(args.storage_region)
        self.assertIsNone(args.storage_bucket)
        self.assertIsNone(args.storage_prefix)
        self.assertIsNone(args.storage_secure)
        self.assertIsNone(args.storage_timeout)
        self.assertIsNone(args.plugin_prefix)
        self.assertIsNone(args.plugin_allow)
        self.assertIsNone(args.plugin_deny)
        self.assertIsNone(args.log_config)
        self.assertIsNone(args.log_level)
        self.assertIsNone(args.log_simply)
        self.assertIsNone(args.signature)
        self.assertIsNone(args.access_token_duration)
        self.assertIsNone(args.refresh_token_duration)
        self.assertIsNone(args.public_signup)
        self.assertIsNone(args.install_uvloop)
        self.assertIsNone(args.teardown)
        self.assertIsNone(args.verbose)
        self.assertIsNone(args.developer)

        with self.assertRaises(AttributeError):
            self.assertIsNone(args.__unknown_variable__)


if __name__ == "__main__":
    main()
