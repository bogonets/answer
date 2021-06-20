# -*- coding: utf-8 -*-

from unittest import main
from tester import AsyncContextTaskTestCase
from recc.variables.storage_names import WORKING_NAME, PYTHON_NAME, VENV_NAME


class ContextTaskTestCase(AsyncContextTaskTestCase):
    async def test_echo(self):
        echo_message = "Hello, World!"
        self.assertEqual(echo_message, await self.client.echo(echo_message))

    async def test_get_workspace_subdir(self):
        names = await self.client.get_workspace_subdir()
        self.assertLessEqual(3, len(names))
        self.assertIn(WORKING_NAME, names)
        self.assertIn(PYTHON_NAME, names)
        self.assertIn(VENV_NAME, names)


if __name__ == "__main__":
    main()
