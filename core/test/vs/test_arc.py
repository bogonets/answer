# -*- coding: utf-8 -*-

import unittest

from recc.vs.arc import Arc
from recc.vs.box import Box


class ArcTestCase(unittest.TestCase):
    def test_arc(self):
        arc0 = Arc(7, 10, 20, "node0.back", "node1.front")
        self.assertEqual(7, arc0.key)
        self.assertEqual("node0.back-node1.front", arc0.fullname)
        self.assertEqual(10, arc0.back_key)
        self.assertEqual(20, arc0.front_key)
        self.assertEqual("node0.back", arc0.back_fullname)
        self.assertEqual("node1.front", arc0.front_fullname)
        self.assertEqual("node0.back-node1.front", str(arc0))
        self.assertEqual("Arc(7)[node0.back-node1.front]", repr(arc0))
        self.assertFalse(arc0.box.exist_data())

    def test_box_sharing(self):
        box = Box(10)
        arc0 = Arc(0, 10, 20, "node0.back", "node1.front", box=box)
        arc1 = Arc(1, 11, 21, "node2.back", "node3.front", box=box)
        self.assertEqual(10, arc0.box.data)
        self.assertEqual(10, arc1.box.data)

        box.set_data(200)
        self.assertEqual(200, arc0.box.data)
        self.assertEqual(200, arc1.box.data)

        arc1.set_box(500)
        self.assertEqual(200, arc0.box.data)
        self.assertEqual(500, arc1.box.data)

    def test_split_merge(self):
        fullname = "node0.back-node1.front"
        names = Arc.split(fullname)
        self.assertEqual(2, len(names))
        self.assertEqual("node0.back", names[0])
        self.assertEqual("node1.front", names[1])
        self.assertEqual(fullname, Arc.merge(names[0], names[1]))


if __name__ == "__main__":
    unittest.main()
