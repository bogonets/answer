# -*- coding: utf-8 -*-

from unittest import main

import numpy as np

from recc.blueprint.blueprint import BpTask
from recc.blueprint.v1.converter import bp_converter
from recc.vs.box import BoxRequest
from tester.samples.read_samples import read_sample_json
from tester.unittest.rpc_test_case import RpcTestCase


class SetGraphNumpy2TestCase(RpcTestCase):
    async def test_set_graph_numpy1(self):
        json = read_sample_json("set_graph.numpy2.json")
        self.assertIsInstance(json, dict)

        graph = bp_converter(json)
        self.assertIsNotNone(graph.tasks)
        self.assertEqual(1, len(graph.tasks))
        task = next(iter(graph.tasks.values()))
        self.assertIsInstance(task, BpTask)
        await self.client.set_task_blueprint(task)

        node1 = "numpy/Builtin/numpy/numpy_array2"
        node1_slot1 = "elements"
        response_data = await self.client.get_node_property(node1, node1_slot1)
        self.assertEqual("1,2,3,4", response_data)

        update_data = "3,2,1,0"
        await self.client.set_node_property(node1, node1_slot1, update_data)
        response_data2 = await self.client.get_node_property(node1, node1_slot1)
        self.assertEqual(update_data, response_data2)

        node2 = "numpy/Builtin/numpy/numpy_size3"
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
