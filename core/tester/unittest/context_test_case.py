# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase
from asyncio import get_event_loop
from tempfile import TemporaryDirectory
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.core.context import Context
from tester.lamda.numpy_plugins import copy_builtin_numpy_nodes


class ContextTestCase(IsolatedAsyncioTestCase):
    async def _setup(self):
        self.temp_dir = TemporaryDirectory()

        config = parse_arguments_to_core_config()
        config.database_name = "recc.test"
        config.storage_root = self.temp_dir.name
        config.teardown = True
        self.context = Context(config, loop=get_event_loop())
        await self.context.open()
        self.assertTrue(self.context.is_database_open())
        self.assertTrue(self.context.is_container_open())
        self.assertTrue(self.context.is_cache_open())

        template_dir = self.context.storage.get_template_directory()
        self.numpy_template_jsons = copy_builtin_numpy_nodes(template_dir)
        self.assertLess(0, len(self.numpy_template_jsons))
        self.context.storage.refresh_templates()

        self.group_slug = "test_group"
        self.project_slug = "test_project"
        self.task_slug = "test_task"

        self.group_uid = await self.context.database.insert_group(self.group_slug)
        self.project_uid = await self.context.database.insert_project(
            self.group_uid, self.project_slug
        )

        self.client = await self.context.run_task(
            self.group_slug, self.project_slug, self.task_slug
        )

    async def asyncSetUp(self):
        try:
            await self._setup()
        except:  # noqa
            await self._teardown()
            raise

    async def _teardown(self):
        try:
            logs = await self.context.log_task(
                self.group_slug, self.project_slug, self.task_slug
            )
            messages: str
            if isinstance(logs, bytes):
                messages = str(logs, encoding="utf-8")
            elif isinstance(logs, str):
                messages = logs
            else:
                messages = str(logs)
            if messages:
                print("Task logging:", messages)
            else:
                print("Empty task logging.")
        except BaseException as e:
            print("Task logging error:", e)

        await self.context.remove_task(
            self.group_slug, self.project_slug, self.task_slug
        )
        await self.context.close()
        self.temp_dir.cleanup()

    async def asyncTearDown(self):
        await self._teardown()
