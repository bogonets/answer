# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main
import tempfile
from recc.template.lamda_template import LamdaTemplate
from recc.template.information import Information
from recc.template.controller import Controller
from recc.template.property import Property
from recc.serializable.json import serialize_json_file, deserialize_json_file

SAMPLE_DATA = {
    "info": {"name": "sample"},
    "controls": {"input": "image"},
    "props": {"name": "src"},
}


class LamdaTemplateJsonTestCase(TestCase):
    def test_default_v1(self):
        obj = LamdaTemplate()
        obj.deserialize(1, SAMPLE_DATA)

        self.assertEqual(1, obj.get_version_tuple()[0])
        self.assertIsInstance(obj.information, Information)
        self.assertIsInstance(obj.controller, Controller)
        self.assertIsInstance(obj.properties, list)
        self.assertIsNotNone(obj.information)
        self.assertIsNotNone(obj.controller)
        self.assertEqual(1, len(obj.properties))
        self.assertIsInstance(obj.properties[0], Property)

        self.assertEqual("sample", obj.information.name)
        self.assertEqual(1, len(obj.controller.data_inputs))
        self.assertEqual("image", obj.controller.data_inputs[0].name)
        self.assertIsNone(obj.controller.data_outputs)
        self.assertEqual("src", obj.properties[0].name)

    def test_json_file(self):
        obj = LamdaTemplate()
        obj.deserialize(1, SAMPLE_DATA)
        serialize_data = obj.serialize(1)

        with tempfile.TemporaryDirectory() as temp_dir:
            json_path = os.path.join(temp_dir, "temp.json")
            serialize_json_file(1, serialize_data, json_path)
            obj2 = deserialize_json_file(1, json_path, LamdaTemplate)

            self.assertEqual(1, obj2.get_version_tuple()[0])
            self.assertIsInstance(obj2.information, Information)
            self.assertIsInstance(obj2.controller, Controller)
            self.assertIsInstance(obj2.properties, list)
            self.assertIsNotNone(obj2.information)
            self.assertIsNotNone(obj2.controller)
            self.assertEqual(1, len(obj2.properties))
            self.assertIsInstance(obj2.properties[0], Property)

            self.assertEqual("sample", obj2.information.name)
            self.assertEqual(1, len(obj2.controller.data_inputs))
            self.assertEqual("image", obj2.controller.data_inputs[0].name)
            self.assertIsNone(obj2.controller.data_outputs)
            self.assertEqual("src", obj2.properties[0].name)


if __name__ == "__main__":
    main()
