# -*- coding: utf-8 -*-

import unittest

from recc.vs.node import Node, NodeEdge
from recc.vs.slot import Slot, SlotCategory, SlotDirection


class NodeTestCase(unittest.TestCase):
    def setUp(self):
        self.in_flow = Slot(0, "s0", 0, "n", SlotDirection.Input, SlotCategory.Flow)
        self.out_flow = Slot(1, "s1", 0, "n", SlotDirection.Output, SlotCategory.Flow)
        self.in_data = Slot(2, "s2", 0, "n", SlotDirection.Input, SlotCategory.Data)
        self.out_data = Slot(3, "s3", 0, "n", SlotDirection.Output, SlotCategory.Data)

    def test_default(self):
        node0 = Node(0, "n0", NodeEdge.Begin)
        node1 = Node(1, "n1", NodeEdge.Middle)
        node2 = Node(2, "n2", NodeEdge.End)

        self.assertEqual(0, node0.key)
        self.assertEqual(1, node1.key)
        self.assertEqual(2, node2.key)

        self.assertEqual("n0", node0.name)
        self.assertEqual("n1", node1.name)
        self.assertEqual("n2", node2.name)

        self.assertEqual(NodeEdge.Begin, node0.edge)
        self.assertEqual(NodeEdge.Middle, node1.edge)
        self.assertEqual(NodeEdge.End, node2.edge)

    def test_begin_node(self):
        node = Node(0, "n", NodeEdge.Begin)
        self.assertRaises(AssertionError, node.add_in_flow, self.in_flow)
        self.assertRaises(AssertionError, node.add_in_flow, self.out_flow)
        self.assertRaises(AssertionError, node.add_in_flow, self.in_data)
        self.assertRaises(AssertionError, node.add_in_flow, self.out_data)

        self.assertRaises(AssertionError, node.add_out_flow, self.in_flow)
        node.add_out_flow(self.out_flow)
        self.assertRaises(AssertionError, node.add_out_flow, self.in_data)
        self.assertRaises(AssertionError, node.add_out_flow, self.out_data)

        self.assertRaises(AssertionError, node.add_in_data, self.in_flow)
        self.assertRaises(AssertionError, node.add_in_data, self.out_flow)
        node.add_in_data(self.in_data)
        self.assertRaises(AssertionError, node.add_in_data, self.out_data)

        self.assertRaises(AssertionError, node.add_out_data, self.in_flow)
        self.assertRaises(AssertionError, node.add_out_data, self.out_flow)
        self.assertRaises(AssertionError, node.add_out_data, self.in_data)
        node.add_out_data(self.out_data)

        self.assertEqual(0, node.get_in_flows_count())
        self.assertEqual(1, node.get_out_flows_count())
        self.assertEqual(1, node.get_in_datas_count())
        self.assertEqual(1, node.get_out_datas_count())
        self.assertEqual(3, node.get_slot_count())
        self.assertEqual(1, node.get_inputs_count())
        self.assertEqual(2, node.get_outputs_count())

        self.assertRaises(KeyError, node.remove_slot, self.in_flow)
        node.remove_slot(self.out_flow)
        node.remove_slot(self.in_data)
        node.remove_slot(self.out_data)
        self.assertEqual(0, node.get_in_flows_count())
        self.assertEqual(0, node.get_out_flows_count())
        self.assertEqual(0, node.get_in_datas_count())
        self.assertEqual(0, node.get_out_datas_count())
        self.assertEqual(0, node.get_slot_count())
        self.assertEqual(0, node.get_inputs_count())
        self.assertEqual(0, node.get_outputs_count())

    def test_middle_node(self):
        node = Node(0, "n", NodeEdge.Middle)
        node.add_in_flow(self.in_flow)
        self.assertRaises(AssertionError, node.add_in_flow, self.out_flow)
        self.assertRaises(AssertionError, node.add_in_flow, self.in_data)
        self.assertRaises(AssertionError, node.add_in_flow, self.out_data)

        self.assertRaises(AssertionError, node.add_out_flow, self.in_flow)
        node.add_out_flow(self.out_flow)
        self.assertRaises(AssertionError, node.add_out_flow, self.in_data)
        self.assertRaises(AssertionError, node.add_out_flow, self.out_data)

        self.assertRaises(AssertionError, node.add_in_data, self.in_flow)
        self.assertRaises(AssertionError, node.add_in_data, self.out_flow)
        node.add_in_data(self.in_data)
        self.assertRaises(AssertionError, node.add_in_data, self.out_data)

        self.assertRaises(AssertionError, node.add_out_data, self.in_flow)
        self.assertRaises(AssertionError, node.add_out_data, self.out_flow)
        self.assertRaises(AssertionError, node.add_out_data, self.in_data)
        node.add_out_data(self.out_data)

        self.assertEqual(1, node.get_in_flows_count())
        self.assertEqual(1, node.get_out_flows_count())
        self.assertEqual(1, node.get_in_datas_count())
        self.assertEqual(1, node.get_out_datas_count())
        self.assertEqual(4, node.get_slot_count())
        self.assertEqual(2, node.get_inputs_count())
        self.assertEqual(2, node.get_outputs_count())

        node.remove_slot(self.in_flow)
        node.remove_slot(self.out_flow)
        node.remove_slot(self.in_data)
        node.remove_slot(self.out_data)
        self.assertEqual(0, node.get_in_flows_count())
        self.assertEqual(0, node.get_out_flows_count())
        self.assertEqual(0, node.get_in_datas_count())
        self.assertEqual(0, node.get_out_datas_count())
        self.assertEqual(0, node.get_slot_count())
        self.assertEqual(0, node.get_inputs_count())
        self.assertEqual(0, node.get_outputs_count())

    def test_end_node(self):
        node = Node(0, "n", NodeEdge.End)
        node.add_in_flow(self.in_flow)
        self.assertRaises(AssertionError, node.add_in_flow, self.out_flow)
        self.assertRaises(AssertionError, node.add_in_flow, self.in_data)
        self.assertRaises(AssertionError, node.add_in_flow, self.out_data)

        self.assertRaises(AssertionError, node.add_out_flow, self.in_flow)
        self.assertRaises(AssertionError, node.add_out_flow, self.out_flow)
        self.assertRaises(AssertionError, node.add_out_flow, self.in_data)
        self.assertRaises(AssertionError, node.add_out_flow, self.out_data)

        self.assertRaises(AssertionError, node.add_in_data, self.in_flow)
        self.assertRaises(AssertionError, node.add_in_data, self.out_flow)
        node.add_in_data(self.in_data)
        self.assertRaises(AssertionError, node.add_in_data, self.out_data)

        self.assertRaises(AssertionError, node.add_out_data, self.in_flow)
        self.assertRaises(AssertionError, node.add_out_data, self.out_flow)
        self.assertRaises(AssertionError, node.add_out_data, self.in_data)
        node.add_out_data(self.out_data)

        self.assertEqual(1, node.get_in_flows_count())
        self.assertEqual(0, node.get_out_flows_count())
        self.assertEqual(1, node.get_in_datas_count())
        self.assertEqual(1, node.get_out_datas_count())
        self.assertEqual(3, node.get_slot_count())
        self.assertEqual(2, node.get_inputs_count())
        self.assertEqual(1, node.get_outputs_count())

        node.remove_slot(self.in_flow)
        self.assertRaises(KeyError, node.remove_slot, self.out_flow)
        node.remove_slot(self.in_data)
        node.remove_slot(self.out_data)
        self.assertEqual(0, node.get_in_flows_count())
        self.assertEqual(0, node.get_out_flows_count())
        self.assertEqual(0, node.get_in_datas_count())
        self.assertEqual(0, node.get_out_datas_count())
        self.assertEqual(0, node.get_slot_count())
        self.assertEqual(0, node.get_inputs_count())
        self.assertEqual(0, node.get_outputs_count())


if __name__ == "__main__":
    unittest.main()
