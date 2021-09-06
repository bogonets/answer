# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.command import get_available_commands


class CommandTestCase(TestCase):
    def test_get_available_commands(self):
        commands = get_available_commands()
        self.assertEqual(3, len(commands))
        self.assertIn("core", commands)
        self.assertIn("task", commands)
        self.assertIn("ctrl", commands)


if __name__ == "__main__":
    main()
