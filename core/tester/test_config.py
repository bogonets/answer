# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.config import Config


class ConfigTestCase(TestCase):
    def test_release_keys(self):
        config_keys = vars(Config.default()).keys()
        release_keys = Config.release_keys()
        self.assertIsInstance(release_keys, list)
        self.assertLess(0, len(release_keys))
        for key in release_keys:
            self.assertIn(key, config_keys)


if __name__ == "__main__":
    main()
