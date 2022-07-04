# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.blueprint.blueprint import BpArc, BpGraph, BpNode, BpProperty, BpSlot, BpTask
from recc.serialization.deserialize import deserialize
from recc.serialization.serialize import serialize


class BlueprintTestCase(TestCase):
    def test_slot(self):
        data = {"node": "Node1", "slot": "Slot1"}
        obj = deserialize(data, BpSlot)
        self.assertEqual("Node1", obj.node)
        self.assertEqual("Slot1", obj.slot)

        serialize_data = serialize(obj)
        self.assertEqual(data, serialize_data)

    def test_arc(self):
        data = {
            "back": {"node": "Node1", "slot": "Slot1"},
            "front": {"node": "Node2", "slot": "Slot2"},
        }
        obj = deserialize(data, BpArc)
        self.assertEqual("Node1", obj.back.node)
        self.assertEqual("Slot1", obj.back.slot)
        self.assertEqual("Node2", obj.front.node)
        self.assertEqual("Slot2", obj.front.slot)

        serialize_data = serialize(obj)
        self.assertEqual(data, serialize_data)

    def test_property(self):
        data = {"value": 100}
        obj = deserialize(data, BpProperty)
        self.assertEqual(100, obj.value)

        serialize_data = serialize(obj)
        self.assertEqual(data, serialize_data)

    def test_node(self):
        data = {
            "template_category": "av",
            "template_name": "av.stream",
            "properties": {
                "index": {"value": 100},
                "url": {"value": "localhost"},
            },
        }
        obj = deserialize(data, BpNode)
        self.assertEqual("av", obj.template_category)
        self.assertEqual("av.stream", obj.template_name)
        self.assertEqual(2, len(obj.properties))
        self.assertEqual(100, obj.properties["index"].value)
        self.assertEqual("localhost", obj.properties["url"].value)

        serialize_data = serialize(obj)
        self.assertEqual(data, serialize_data)

    def test_task(self):
        data = {
            "nodes": {
                "Node1": {
                    "properties": {
                        "index": {"value": 100},
                    },
                },
                "Node2": {},
            },
            "arcs": {
                "Link1": {
                    "back": {"node": "Node1", "slot": "Slot1"},
                    "front": {"node": "Node2", "slot": "Slot2"},
                },
            },
        }
        obj = deserialize(data, BpTask)
        self.assertEqual(2, len(obj.nodes))
        self.assertEqual(1, len(obj.nodes["Node1"].properties))
        self.assertEqual(100, obj.nodes["Node1"].properties["index"].value)
        self.assertIsNone(obj.nodes["Node2"].properties)
        self.assertEqual(1, len(obj.arcs))
        self.assertEqual("Node1", obj.arcs["Link1"].back.node)
        self.assertEqual("Slot1", obj.arcs["Link1"].back.slot)
        self.assertEqual("Node2", obj.arcs["Link1"].front.node)
        self.assertEqual("Slot2", obj.arcs["Link1"].front.slot)

        serialize_data = serialize(obj)
        self.assertEqual(data, serialize_data)

    def test_graph(self):
        data = {
            "tasks": {
                "Task1": {
                    "nodes": {
                        "Node1": {
                            "properties": {
                                "index": {"value": 100},
                            },
                        },
                        "Node2": {},
                    },
                    "arcs": {
                        "Link1": {
                            "back": {"node": "Node1", "slot": "Slot1"},
                            "front": {"node": "Node2", "slot": "Slot2"},
                        },
                    },
                },
            },
        }
        obj = deserialize(data, BpGraph)
        self.assertEqual(1, len(obj.tasks))

        task = obj.tasks["Task1"]
        self.assertEqual(2, len(task.nodes))
        self.assertEqual(1, len(task.nodes["Node1"].properties))
        self.assertEqual(100, task.nodes["Node1"].properties["index"].value)
        self.assertIsNone(task.nodes["Node2"].properties)
        self.assertEqual(1, len(task.arcs))
        self.assertEqual("Node1", task.arcs["Link1"].back.node)
        self.assertEqual("Slot1", task.arcs["Link1"].back.slot)
        self.assertEqual("Node2", task.arcs["Link1"].front.node)
        self.assertEqual("Slot2", task.arcs["Link1"].front.slot)

        serialize_data = serialize(obj)
        self.assertEqual(data, serialize_data)


if __name__ == "__main__":
    main()
