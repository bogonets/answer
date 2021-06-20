# -*- coding: utf-8 -*-

import unittest
from recc.vs.slot import SlotDirection, SlotCategory, Slot
from recc.vs.slot_machine import SlotMachine


class SlotMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.in_flow = Slot(0, "s0", 0, "n0", SlotDirection.Input, SlotCategory.Flow)
        self.out_flow = Slot(1, "s1", 1, "n1", SlotDirection.Output, SlotCategory.Flow)
        self.in_data = Slot(2, "s2", 2, "n2", SlotDirection.Input, SlotCategory.Data)
        self.out_data = Slot(3, "s3", 3, "n3", SlotDirection.Output, SlotCategory.Data)

    def test_default(self):
        sm = SlotMachine()

        self.assertRaises(AssertionError, sm.add_in_data, self.in_flow)
        self.assertRaises(AssertionError, sm.add_in_data, self.out_flow)
        sm.add_in_data(self.in_data)
        self.assertRaises(AssertionError, sm.add_in_data, self.out_data)
        self.assertEqual(0, sm.get_in_flows_count())
        self.assertEqual(0, sm.get_out_flows_count())
        self.assertEqual(1, sm.get_in_datas_count())
        self.assertEqual(0, sm.get_out_datas_count())
        self.assertEqual(1, sm.get_slot_count())
        self.assertEqual(1, sm.get_inputs_count())
        self.assertEqual(0, sm.get_outputs_count())

        self.assertRaises(AssertionError, sm.add_out_data, self.in_flow)
        self.assertRaises(AssertionError, sm.add_out_data, self.out_flow)
        self.assertRaises(AssertionError, sm.add_out_data, self.in_data)
        sm.add_out_data(self.out_data)
        self.assertEqual(0, sm.get_in_flows_count())
        self.assertEqual(0, sm.get_out_flows_count())
        self.assertEqual(1, sm.get_in_datas_count())
        self.assertEqual(1, sm.get_out_datas_count())
        self.assertEqual(2, sm.get_slot_count())
        self.assertEqual(1, sm.get_inputs_count())
        self.assertEqual(1, sm.get_outputs_count())

        sm.add_in_flow(self.in_flow)
        self.assertRaises(AssertionError, sm.add_in_flow, self.out_flow)
        self.assertRaises(AssertionError, sm.add_in_flow, self.in_data)
        self.assertRaises(AssertionError, sm.add_in_flow, self.out_data)
        self.assertEqual(1, sm.get_in_flows_count())
        self.assertEqual(0, sm.get_out_flows_count())
        self.assertEqual(1, sm.get_in_datas_count())
        self.assertEqual(1, sm.get_out_datas_count())
        self.assertEqual(3, sm.get_slot_count())
        self.assertEqual(2, sm.get_inputs_count())
        self.assertEqual(1, sm.get_outputs_count())

        self.assertRaises(AssertionError, sm.add_out_flow, self.in_flow)
        sm.add_out_flow(self.out_flow)
        self.assertRaises(AssertionError, sm.add_out_flow, self.in_data)
        self.assertRaises(AssertionError, sm.add_out_flow, self.out_data)
        self.assertEqual(1, sm.get_in_flows_count())
        self.assertEqual(1, sm.get_out_flows_count())
        self.assertEqual(1, sm.get_in_datas_count())
        self.assertEqual(1, sm.get_out_datas_count())
        self.assertEqual(4, sm.get_slot_count())
        self.assertEqual(2, sm.get_inputs_count())
        self.assertEqual(2, sm.get_outputs_count())

        self.assertTrue(sm.exist_slot(self.in_flow.key))
        self.assertTrue(sm.exist_slot(self.out_flow.key))
        self.assertTrue(sm.exist_slot(self.in_data.key))
        self.assertTrue(sm.exist_slot(self.out_data.key))

        sm.remove_slot(self.in_flow.key)
        self.assertEqual(0, sm.get_in_flows_count())
        self.assertEqual(1, sm.get_out_flows_count())
        self.assertEqual(1, sm.get_in_datas_count())
        self.assertEqual(1, sm.get_out_datas_count())
        self.assertEqual(3, sm.get_slot_count())
        self.assertEqual(1, sm.get_inputs_count())
        self.assertEqual(2, sm.get_outputs_count())

        sm.remove_slot(self.out_flow.key)
        self.assertEqual(0, sm.get_in_flows_count())
        self.assertEqual(0, sm.get_out_flows_count())
        self.assertEqual(1, sm.get_in_datas_count())
        self.assertEqual(1, sm.get_out_datas_count())
        self.assertEqual(2, sm.get_slot_count())
        self.assertEqual(1, sm.get_inputs_count())
        self.assertEqual(1, sm.get_outputs_count())

        sm.remove_slot(self.in_data.key)
        self.assertEqual(0, sm.get_in_flows_count())
        self.assertEqual(0, sm.get_out_flows_count())
        self.assertEqual(0, sm.get_in_datas_count())
        self.assertEqual(1, sm.get_out_datas_count())
        self.assertEqual(1, sm.get_slot_count())
        self.assertEqual(0, sm.get_inputs_count())
        self.assertEqual(1, sm.get_outputs_count())

        sm.remove_slot(self.out_data.key)
        self.assertEqual(0, sm.get_in_flows_count())
        self.assertEqual(0, sm.get_out_flows_count())
        self.assertEqual(0, sm.get_in_datas_count())
        self.assertEqual(0, sm.get_out_datas_count())
        self.assertEqual(0, sm.get_slot_count())
        self.assertEqual(0, sm.get_inputs_count())
        self.assertEqual(0, sm.get_outputs_count())


if __name__ == "__main__":
    unittest.main()
