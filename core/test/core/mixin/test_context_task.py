# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.context_test_case import ContextTestCase
from recc.variables.storage import CORE_TEMPLATE_NAME, WORKSPACE_VENV_NAME


class ContextTaskTestCase(ContextTestCase):
    async def test_echo(self):
        echo_message = "Hello, World!"
        self.assertEqual(echo_message, await self.client.echo(echo_message))

    async def test_get_workspace_subdir(self):
        names = await self.client.get_workspace_subdir()
        self.assertLessEqual(3, len(names))
        self.assertIn(CORE_TEMPLATE_NAME, names)
        self.assertIn(WORKSPACE_VENV_NAME, names)


if __name__ == "__main__":
    main()
