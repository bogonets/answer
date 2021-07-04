# -*- coding: utf-8 -*-

import os
import asyncio
import numpy as np
import shutil
from unittest import main
from tempfile import TemporaryDirectory
from datetime import datetime, timedelta
from recc.argparse.default_namespace import get_default_task_config
from recc.blueprint.blueprint import BpTask
from recc.blueprint.v1.converter import bp_converter
from recc.rpc.rpc_client import create_rpc_client
from recc.task.task_server import create_task_server
from recc.variables.storage import CORE_TEMPLATE_NAME, WORKSPACE_VENV_NAME
from recc.vs.box import BoxRequest
from tester import AsyncTestCase, read_sample_json
from tester.node.numpy_plugins import copy_builtin_numpy_nodes


class RpcTestCase(AsyncTestCase):
    async def _setup(self):
        self.temp_dir = TemporaryDirectory()

        self.config = get_default_task_config()
        self.config.task_address = "[::]:0"
        self.config.task_register = "__unknown_key__"
        self.config.task_workspace_dir = self.temp_dir.name

        server_info = create_task_server(self.config)
        self.servicer = server_info.servicer
        self.server = server_info.server
        self.port = server_info.accepted_port_number
        self.address = f"localhost:{self.port}"
        self.client = create_rpc_client(self.address)

        self.template_dir = self.servicer.storage.get_template_directory()
        self.numpy_template_jsons = copy_builtin_numpy_nodes(self.template_dir)
        self.assertLess(0, len(self.numpy_template_jsons))
        self.servicer.storage.refresh_templates()

        await self.server.start()
        await self.client.open()
        self.assertTrue(self.client.is_open())

    async def setUp(self):
        try:
            await self._setup()
        except:  # noqa
            await self._teardown()
            raise

    async def _teardown(self):
        await self.client.close()
        await self.server.stop(None)
        self.temp_dir.cleanup()
        self.assertFalse(self.client.is_open())

    async def tearDown(self):
        await self._teardown()

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
        self.assertIn(CORE_TEMPLATE_NAME, names)
        self.assertIn(WORKSPACE_VENV_NAME, names)

    async def test_get_template_names(self):
        names = await self.client.get_template_names()
        self.assertLess(0, len(names))

    async def test_upload_templates(self):
        data = self.servicer.storage.compress_templates()

        # Remove templates.
        shutil.rmtree(self.template_dir)
        os.mkdir(self.template_dir)
        self.assertTrue(os.path.isdir(self.template_dir))
        self.assertEqual(0, len(os.listdir(self.template_dir)))

        self.servicer.storage.refresh_templates()
        save_template_count = len(await self.client.get_template_names())

        await self.client.upload_templates(data)
        next_template_count = len(await self.client.get_template_names())
        self.assertLess(save_template_count, next_template_count)

    async def test_set_task_blueprint(self):
        json = read_sample_json("set_graph.numpy.v1.data.json")
        self.assertIsInstance(json, dict)

        graph = bp_converter(json)
        self.assertIsNotNone(graph.tasks)
        self.assertEqual(1, len(graph.tasks))
        task = next(iter(graph.tasks.values()))
        self.assertIsInstance(task, BpTask)
        await self.client.set_task_blueprint(task)

        node1 = "numpy/numpy_array2"
        node1_slot1 = "elements"
        response_data = await self.client.get_node_property(node1, node1_slot1)
        self.assertEqual("0,1,2,3", response_data)

        update_data = "3,2,1,0"
        await self.client.set_node_property(node1, node1_slot1, update_data)
        response_data2 = await self.client.get_node_property(node1, node1_slot1)
        self.assertEqual(update_data, response_data2)

        node2 = "numpy/numpy_size3"
        node2_slot1 = "result"
        box_request = [BoxRequest(node2, node2_slot1)]
        signal_result = await self.client.send_signal(None, None, box_request)
        self.assertEqual(1, len(signal_result))
        result_data = signal_result[0]
        self.assertEqual(node2, result_data.node)
        self.assertEqual(node2_slot1, result_data.slot)
        self.assertIsInstance(result_data.data, np.ndarray)
        self.assertEqual(4, int(result_data.data[0]))


if __name__ == "__main__":
    main()
