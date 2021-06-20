# -*- coding: utf-8 -*-

import unittest
from recc.vs.box import BoxState, Box


class BoxTestCase(unittest.TestCase):
    def test_box(self):
        box0 = Box()
        self.assertEqual("Data<NoneType>[Inactive]", repr(box0))
        self.assertIsNone(box0.data)
        self.assertEqual(type(None), box0.data_type)
        self.assertEqual("NoneType", box0.data_type_name)
        self.assertEqual(BoxState.Inactive, box0.state)
        self.assertEqual("Inactive", box0.state_name)
        self.assertFalse(box0.exist_data())

        box0.inactive()
        self.assertTrue(box0.is_inactive())
        box0.active()
        self.assertTrue(box0.is_active())
        box0.skip()
        self.assertTrue(box0.is_skip())
        box0.failure()
        self.assertTrue(box0.is_failure())

        box0.set_data(200)
        self.assertEqual(200, box0.data)
        self.assertEqual(int, box0.data_type)
        self.assertEqual("int", box0.data_type_name)

    def test_box_sharing(self):
        box0 = Box()
        box1 = box0
        self.assertIsNone(box0.data)
        self.assertIsNone(box1.data)
        self.assertFalse(box0.exist_data())
        self.assertFalse(box1.exist_data())
        self.assertEqual(BoxState.Inactive, box0.state)
        self.assertEqual(BoxState.Inactive, box1.state)

        box0.set_data(100)
        self.assertEqual(100, box0.data)
        self.assertEqual(100, box1.data)
        self.assertTrue(box0.exist_data())
        self.assertTrue(box1.exist_data())

        box0.active()
        self.assertEqual(BoxState.Active, box0.state)
        self.assertEqual(BoxState.Active, box1.state)


if __name__ == "__main__":
    unittest.main()
