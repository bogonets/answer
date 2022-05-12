# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.control import Control
from recc.template.controller import Controller


class TemplateControllerTestCase(TestCase):
    def test_default_v1(self):
        input1 = Control()
        input1.name = "i1"
        input1.mimes = ["json"]
        input2 = Control()
        input2.name = "i2"
        input2.mimes = ["text"]
        output1 = Control()
        output1.name = "o1"
        output1.mimes = ["jpeg", "png"]
        output2 = Control()
        output2.name = "o2"
        obj = Controller()
        obj.data_inputs = [input1, input2]
        obj.data_outputs = [output1, output2]
        data = obj.serialize(1)

        self.assertEqual(2, len(data))

        inputs = data["input"]
        outputs = data["output"]
        self.assertFalse(inputs["dynamic"])
        self.assertFalse(outputs["dynamic"])
        self.assertEqual("numpy", inputs["method"])
        self.assertEqual("numpy", outputs["method"])
        self.assertEqual(2, len(inputs["list"]))
        self.assertEqual(2, len(outputs["list"]))

        self.assertEqual({"name": "i1", "mimes": ["json"]}, inputs["list"][0])
        self.assertEqual({"name": "i2", "mimes": ["text"]}, inputs["list"][1])
        self.assertEqual({"name": "o1", "mimes": ["jpeg", "png"]}, outputs["list"][0])
        self.assertEqual({"name": "o2"}, outputs["list"][1])

        obj.deserialize(1, data)
        self.assertEqual(2, len(obj.data_inputs))
        self.assertEqual(2, len(obj.data_outputs))
        self.assertEqual("i1", obj.data_inputs[0].name)
        self.assertEqual(["json"], obj.data_inputs[0].mimes)
        self.assertEqual("i2", obj.data_inputs[1].name)
        self.assertEqual(["text"], obj.data_inputs[1].mimes)
        self.assertEqual("o1", obj.data_outputs[0].name)
        self.assertEqual(["jpeg", "png"], obj.data_outputs[0].mimes)
        self.assertEqual("o2", obj.data_outputs[1].name)
        self.assertIsNone(obj.data_outputs[1].mimes)

    def test_simple_str_v1(self):
        data = {"input": "i1"}
        obj = Controller()
        obj.deserialize(1, data)
        self.assertIsInstance(obj.data_inputs, list)
        self.assertIsNone(obj.data_outputs)
        self.assertEqual(1, len(obj.data_inputs))
        self.assertEqual("i1", obj.data_inputs[0].name)

    def test_simple_list_str_only_v1(self):
        data = {"input": ["i1", "i2"]}
        obj = Controller()
        obj.deserialize(1, data)
        self.assertIsInstance(obj.data_inputs, list)
        self.assertIsNone(obj.data_outputs)
        self.assertEqual(2, len(obj.data_inputs))
        self.assertEqual("i1", obj.data_inputs[0].name)
        self.assertEqual("i2", obj.data_inputs[1].name)

    def test_simple_dict_str_v1(self):
        data = {"output": {"list": "o1"}}
        obj = Controller()
        obj.deserialize(1, data)
        self.assertIsNone(obj.data_inputs)
        self.assertIsInstance(obj.data_outputs, list)
        self.assertEqual(1, len(obj.data_outputs))
        self.assertEqual("o1", obj.data_outputs[0].name)

    def test_simple_dict_dict_v1(self):
        data = {
            "output": {
                "dynamic": False,
                "method": "numpy",
                "list": {"name": "o1"},
            },
        }
        obj = Controller()
        obj.deserialize(1, data)
        self.assertIsNone(obj.data_inputs)
        self.assertIsInstance(obj.data_outputs, list)
        self.assertEqual(1, len(obj.data_outputs))
        self.assertEqual("o1", obj.data_outputs[0].name)

    def test_simple_dict_list_dict_v1(self):
        data = {
            "output": {
                "dynamic": False,
                "method": "numpy",
                "list": [
                    {"name": "o1"},
                ],
            },
        }
        obj = Controller()
        obj.deserialize(1, data)
        self.assertIsNone(obj.data_inputs)
        self.assertIsInstance(obj.data_outputs, list)
        self.assertEqual(1, len(obj.data_outputs))
        self.assertEqual("o1", obj.data_outputs[0].name)

    def test_default_v2(self):
        input1 = Control()
        input1.name = "i1"
        input1.mimes = ["json"]
        output1 = Control()
        output1.name = "o1"
        output1.mimes = ["jpeg", "png"]
        obj = Controller()
        obj.data_inputs = [input1]
        obj.data_outputs = [output1]
        data = obj.serialize(2)

        self.assertEqual(2, len(data))

        inputs = data["data_inputs"]
        outputs = data["data_outputs"]
        self.assertEqual(1, len(inputs))
        self.assertEqual(1, len(outputs))

        self.assertEqual({"name": "i1", "mimes": ["json"]}, inputs[0])
        self.assertEqual({"name": "o1", "mimes": ["jpeg", "png"]}, outputs[0])

        obj.deserialize(2, data)
        self.assertEqual(1, len(obj.data_inputs))
        self.assertEqual(1, len(obj.data_outputs))
        self.assertEqual("i1", obj.data_inputs[0].name)
        self.assertEqual(["json"], obj.data_inputs[0].mimes)
        self.assertEqual("o1", obj.data_outputs[0].name)
        self.assertEqual(["jpeg", "png"], obj.data_outputs[0].mimes)


if __name__ == "__main__":
    main()
