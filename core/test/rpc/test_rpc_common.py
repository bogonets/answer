# -*- coding: utf-8 -*-

import os
import asyncio
import numpy as np
from unittest import main
from tester.unittest.rpc_test_case import RpcTestCase
from tester.lamda.numpy_plugins import copy_builtin_numpy_nodes
from datetime import datetime, timedelta
from recc.variables.storage import LOCAL_STORAGE_TEMPLATE_NAME, TASK_STORAGE_VENV_NAME
from recc.file.remove import remove_recursively


class RpcCommonTestCase(RpcTestCase):
    async def test_heartbeat(self):
        self.assertTrue(await self.client.heartbeat(0))

    async def test_multiple_heartbeat(self):
        before = datetime.now()
        f1 = asyncio.ensure_future(self.client.heartbeat(1))
        f2 = asyncio.ensure_future(self.client.heartbeat(1))
        f3 = asyncio.ensure_future(self.client.heartbeat(1))
        f4 = asyncio.ensure_future(self.client.heartbeat(1))
        await asyncio.gather(f1, f2, f3, f4)
        self.assertTrue(f1.result())
        self.assertTrue(f2.result())
        self.assertTrue(f3.result())
        self.assertTrue(f4.result())
        after = datetime.now()
        self.assertGreater(timedelta(seconds=4), after - before)

    async def test_echo(self):
        msg = "Hello, World!"
        self.assertEqual(msg, await self.client.echo(msg))

    async def test_multiple_echo(self):
        msg1 = "Message 01"
        msg2 = "Message 02"
        msg3 = "Message 03"
        msg4 = "Message 04"
        before = datetime.now()
        f1 = asyncio.ensure_future(self.client.echo(msg1))
        f2 = asyncio.ensure_future(self.client.echo(msg2))
        f3 = asyncio.ensure_future(self.client.echo(msg3))
        f4 = asyncio.ensure_future(self.client.echo(msg4))
        await asyncio.gather(f1, f2, f3, f4)
        self.assertEqual(msg1, f1.result())
        self.assertEqual(msg2, f2.result())
        self.assertEqual(msg3, f3.result())
        self.assertEqual(msg4, f4.result())
        after = datetime.now()
        self.assertGreater(timedelta(seconds=4), after - before)

    async def test_echo_data(self):
        data = b"Hello, World!"
        self.assertEqual(data, await self.client.echo_data(data))

    async def _echo_data(self, prefix: str, size: int) -> None:
        data = np.random.bytes(size)
        self.assertIsInstance(data, bytes)
        before = datetime.now()
        response = await self.client.echo_data(data)
        delta = datetime.now() - before
        delta_seconds = delta.total_seconds()
        mb_size = size / 1024.0 / 1024.0
        print(f"{prefix}({mb_size}MB) request/response delta: {delta_seconds}s")
        self.assertEqual(data, response)

    async def test_echo_data_benchmark(self):
        await self._echo_data("nHD RGBA32", 640 * 360 * 4)  # 0.87890625 MByte
        await self._echo_data("qHD RGBA32", 960 * 540 * 4)  # 1.9775390625 MByte
        await self._echo_data("HD RGBA32", 1280 * 720 * 4)  # 3.515625 MByte
        await self._echo_data("FHD RGBA32", 1920 * 1080 * 4)  # 7.91015625 MByte
        await self._echo_data("UHD RGBA32", 3840 * 2160 * 4)  # 31.640625 MByte

    async def test_get_workspace_subdir(self):
        names = await self.client.get_workspace_subdir()
        self.assertLessEqual(3, len(names))
        self.assertIn(LOCAL_STORAGE_TEMPLATE_NAME, names)
        self.assertIn(TASK_STORAGE_VENV_NAME, names)

    async def test_get_template_names(self):
        names = await self.client.get_template_names()
        self.assertLess(0, len(names))

    async def test_upload_templates(self):
        template_dir = self.servicer.workspace.template
        numpy_template_jsons = copy_builtin_numpy_nodes(template_dir)
        self.assertLess(0, len(numpy_template_jsons))
        self.servicer.workspace.refresh_templates()

        data = self.servicer.workspace.compress_templates()

        # Remove templates.
        remove_recursively(template_dir)
        os.mkdir(template_dir)
        self.assertTrue(os.path.isdir(template_dir))
        self.assertEqual(0, len(os.listdir(template_dir)))

        self.servicer.workspace.refresh_templates()
        save_template_count = len(await self.client.get_template_names())

        await self.client.upload_templates(data)
        next_template_count = len(await self.client.get_template_names())
        self.assertLess(save_template_count, next_template_count)


if __name__ == "__main__":
    main()
