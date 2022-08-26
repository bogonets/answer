# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.control import Control
from recc.template.controller import Controller


class TemplateControllerTestCase(TestCase):
    def test_default(self):
        input1 = Control()
        input1.name = "i1"
        input1.mimes = ["json"]
        output1 = Control()
        output1.name = "o1"
        output1.mimes = ["jpeg", "png"]
        obj = Controller()
        obj.data_inputs = [input1]
        obj.data_outputs = [output1]
        data = obj.__serialize__()

        self.assertEqual(2, len(data))

        inputs = data["data_inputs"]
        outputs = data["data_outputs"]
        self.assertEqual(1, len(inputs))
        self.assertEqual(1, len(outputs))

        self.assertEqual({"name": "i1", "mimes": ["json"]}, inputs[0])
        self.assertEqual({"name": "o1", "mimes": ["jpeg", "png"]}, outputs[0])

        obj.__deserialize__(data)
        self.assertEqual(1, len(obj.data_inputs))
        self.assertEqual(1, len(obj.data_outputs))
        self.assertEqual("i1", obj.data_inputs[0].name)
        self.assertEqual(["json"], obj.data_inputs[0].mimes)
        self.assertEqual("o1", obj.data_outputs[0].name)
        self.assertEqual(["jpeg", "png"], obj.data_outputs[0].mimes)


if __name__ == "__main__":
    main()
