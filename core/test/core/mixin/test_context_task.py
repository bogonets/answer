# -*- coding: utf-8 -*-

from unittest import main

from recc.variables.storage import LOCAL_STORAGE_TEMPLATE_NAME, TASK_STORAGE_VENV_NAME
from tester.unittest.context_test_case import ContextTestCase


class ContextTaskTestCase(ContextTestCase):
    async def test_echo(self):
        echo_message = "Hello, World!"
        self.assertEqual(echo_message, await self.client.echo(echo_message))

    async def test_get_workspace_subdir(self):
        names = await self.client.get_workspace_subdir()
        self.assertLessEqual(3, len(names))
        self.assertIn(LOCAL_STORAGE_TEMPLATE_NAME, names)
        self.assertIn(TASK_STORAGE_VENV_NAME, names)


if __name__ == "__main__":
    main()
