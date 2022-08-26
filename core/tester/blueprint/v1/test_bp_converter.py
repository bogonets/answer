# -*- coding: utf-8 -*-

import json
from unittest import TestCase, main

from recc.blueprint.blueprint import BpGraph, BpTask
from recc.blueprint.v1.converter import bp_converter
from tester.samples.read_samples import read_sample


class BpConverterTestCase(TestCase):
    def test_default(self):
        json_text = read_sample("set_graph.v1.data.json")
        self.assertTrue(json_text)

        result = bp_converter(json.loads(json_text))
        self.assertIsInstance(result, BpGraph)

        self.assertEqual(1, len(result.tasks))
        self.assertIn("Task", result.tasks)

        task = result.tasks["Task"]
        self.assertIsNotNone(task)
        self.assertIsInstance(task, BpTask)

        self.assertEqual(3, len(task.nodes))
        imread2 = task.nodes["cv2/cv2_imread2"]
        self.assertEqual("cv2", imread2.template_category)
        self.assertEqual("cv2_imread", imread2.template_name)
        self.assertEqual(2, len(imread2.properties))
        self.assertEqual("color", imread2.properties["flag"].value)
        self.assertEqual("true", imread2.properties["cache"].value)

        cvt_color3 = task.nodes["cv2/cv2_cvt_color3"]
        self.assertEqual("cv2", cvt_color3.template_category)
        self.assertEqual("cv2_cvt_color", cvt_color3.template_name)
        self.assertEqual(1, len(cvt_color3.properties))
        self.assertEqual("BGR2RGB", cvt_color3.properties["flag"].value)

        imwrite4 = task.nodes["cv2/cv2_imwrite4"]
        self.assertEqual("cv2", imwrite4.template_category)
        self.assertEqual("cv2_imwrite", imwrite4.template_name)
        self.assertIsNone(imwrite4.properties)

        self.assertEqual(2, len(task.arcs))
        self.assertEqual("cv2/cv2_imread2", task.arcs["2"].back.node)
        self.assertEqual("result", task.arcs["2"].back.slot)
        self.assertEqual("cv2/cv2_cvt_color3", task.arcs["2"].front.node)
        self.assertEqual("array", task.arcs["2"].front.slot)

        self.assertEqual("cv2/cv2_cvt_color3", task.arcs["3"].back.node)
        self.assertEqual("result", task.arcs["3"].back.slot)
        self.assertEqual("cv2/cv2_imwrite4", task.arcs["3"].front.node)
        self.assertEqual("array", task.arcs["3"].front.slot)


if __name__ == "__main__":
    main()
