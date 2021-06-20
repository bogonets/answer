# -*- coding: utf-8 -*-

import unittest
from recc.vs.box import Box
from recc.vs.arc import Arc
from recc.vs.slot import SlotDirection, SlotCategory, Slot


class SlotTestCase(unittest.TestCase):
    def test_slot(self):
        slot0 = Slot(3, "front", 10, "node0", SlotDirection.Output, SlotCategory.Flow)
        self.assertEqual("Slot(3)[node0.front/Flow/Output/arcs=0]", repr(slot0))
        self.assertEqual("node0.front", slot0.fullname)
        self.assertEqual(3, slot0.key)
        self.assertEqual("front", slot0.name)
        self.assertEqual(10, slot0.base_node_key)
        self.assertEqual("node0", slot0.base_node_name)
        self.assertEqual(SlotDirection.Output, slot0.direction)
        self.assertEqual(SlotCategory.Flow, slot0.category)
        self.assertFalse(slot0.box.exist_data())

        self.assertFalse(slot0.is_optional())
        self.assertTrue(slot0.is_requirement())

        slot0.set_optional()
        self.assertTrue(slot0.is_optional())
        self.assertFalse(slot0.is_requirement())

    def test_box_sharing(self):
        box = Box(10)
        slot0 = Slot(0, "f", 20, "n0", SlotDirection.Output, SlotCategory.Data, box=box)
        slot1 = Slot(1, "b", 21, "n1", SlotDirection.Input, SlotCategory.Data, box=box)
        self.assertEqual(10, slot0.box.data)
        self.assertEqual(10, slot1.box.data)

        box.set_data(200)
        self.assertEqual(200, slot0.box.data)
        self.assertEqual(200, slot1.box.data)

        slot1.set_box(Box(500))
        self.assertEqual(200, slot0.box.data)
        self.assertEqual(500, slot1.box.data)

    def test_split_merge(self):
        fullname = "node0.back"
        names = Slot.split_key(fullname)
        self.assertEqual(2, len(names))
        self.assertEqual("node0", names[0])
        self.assertEqual("back", names[1])
        self.assertEqual(fullname, Slot.create_key(names[0], names[1]))

    def test_mimes(self):
        slot0 = Slot(1, "k", 2, "n", SlotDirection.Input, SlotCategory.Data)
        self.assertEqual(0, len(slot0.mimes))
        slot0.add_mime("application/json")
        self.assertEqual(1, len(slot0.mimes))
        self.assertRaises(KeyError, slot0.remove_mime, "application/text")
        self.assertEqual(1, len(slot0.mimes))
        slot0.remove_mime("application/json")
        self.assertEqual(0, len(slot0.mimes))

    def test_arc(self):
        slot0 = Slot(0, "slot0", 2, "node2", SlotDirection.Output, SlotCategory.Flow)
        slot1 = Slot(1, "slot1", 3, "node3", SlotDirection.Input, SlotCategory.Flow)
        arc10 = Arc(10, 1, 0, "node3.slot1", "node2.slot0")
        self.assertRaises(AssertionError, slot0.add_output_arc, arc10)
        self.assertRaises(AssertionError, slot1.add_input_arc, arc10)
        self.assertEqual(0, len(slot0.arcs))
        self.assertEqual(0, len(slot1.arcs))

        arc11_error = Arc(10, 0, 1, "???.???", "node3.slot1")
        self.assertRaises(AssertionError, slot0.add_output_arc, arc11_error)

        arc12_error = Arc(10, 0, 1, "node2.slot0", "???.???")
        self.assertRaises(AssertionError, slot1.add_input_arc, arc12_error)

        arc_ok = Arc(100, 0, 1, "node2.slot0", "node3.slot1")
        slot0.add_output_arc(arc_ok)
        slot1.add_input_arc(arc_ok)
        self.assertEqual(1, len(slot0.arcs))
        self.assertEqual(1, len(slot1.arcs))

        slot0.remove_arc(100)
        slot1.remove_arc(100)
        self.assertEqual(0, len(slot0.arcs))
        self.assertEqual(0, len(slot1.arcs))


if __name__ == "__main__":
    unittest.main()
