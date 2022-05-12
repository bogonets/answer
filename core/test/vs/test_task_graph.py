# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.vs.task_graph import TaskGraph


class TaskGraphTestCase(TestCase):
    def test_add(self):
        task_name = "test"
        task = TaskGraph(task_name)

        self.assertEqual(0, task.get_node_count())
        self.assertEqual(0, task.get_slot_count())
        self.assertEqual(0, task.get_arc_count())
        self.assertEqual(task_name, task.name)

        node0 = task.add_begin_node("node0")
        node1 = task.add_middle_node("node1")
        node2 = task.add_end_node("node2")

        self.assertEqual(3, task.get_node_count())
        self.assertEqual(1, task.get_begins_count())
        self.assertEqual(1, task.get_middles_count())
        self.assertEqual(1, task.get_ends_count())

        self.assertRaises(ValueError, task.add_input_flow_slot, "0", node0)
        slot1 = task.add_output_flow_slot("1", node0)
        slot2 = task.add_input_data_slot("2", node0)
        slot3 = task.add_output_data_slot("3", node0)

        slot4 = task.add_input_flow_slot("4", node1)
        slot5 = task.add_output_flow_slot("5", node1)
        slot6 = task.add_input_data_slot("6", node1)
        slot7 = task.add_output_data_slot("7", node1)

        slot8 = task.add_input_flow_slot("8", node2)
        self.assertRaises(ValueError, task.add_output_flow_slot, "9", node2)
        slot10 = task.add_input_data_slot("10", node2)
        slot11 = task.add_output_data_slot("11", node2)

        self.assertEqual(10, task.get_slot_count())
        self.assertEqual(5, task.get_inputs_count())
        self.assertEqual(5, task.get_outputs_count())
        self.assertEqual(2, task.get_in_flows_count())
        self.assertEqual(2, task.get_out_flows_count())
        self.assertEqual(3, task.get_in_datas_count())
        self.assertEqual(3, task.get_out_datas_count())

        self.assertRaises(ValueError, task.add_arc, slot1, slot2)
        self.assertRaises(ValueError, task.add_arc, slot1, slot3)
        self.assertRaises(ValueError, task.add_arc, slot2, slot3)
        self.assertRaises(ValueError, task.add_arc, slot2, slot1)
        self.assertRaises(ValueError, task.add_arc, slot3, slot1)
        self.assertRaises(ValueError, task.add_arc, slot3, slot2)

        task.add_arc(slot1, slot4)
        task.add_arc(slot5, slot8)
        self.assertEqual(2, task.get_arc_count())

        self.assertRaises(ValueError, task.add_arc, slot2, slot6)
        self.assertRaises(ValueError, task.add_arc, slot2, slot7)
        task.add_arc(slot3, slot6)
        self.assertRaises(ValueError, task.add_arc, slot3, slot7)

        self.assertRaises(ValueError, task.add_arc, slot6, slot10)
        self.assertRaises(ValueError, task.add_arc, slot6, slot11)
        task.add_arc(slot7, slot10)
        self.assertRaises(ValueError, task.add_arc, slot7, slot11)

        self.assertEqual(4, task.get_arc_count())


if __name__ == "__main__":
    main()
