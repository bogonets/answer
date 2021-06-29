# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.template.lambda_template import LambdaTemplate
from recc.template.information import Information
from recc.template.controller import Controller
from recc.template.property import Property

SAMPLE_DATA = {
    "info": {
        "name": "av_stream_video",
        "version": "1.1.4",
        "category": "av",
        "keywords": ["av"],
        "homepage": "https://answer.bogonets.com/",
        "bugs": "https://answer.bogonets.com/",
        "license": "Bogonet License",
        "author": "zer0",
        "dependencies": [
            {"type": "pip", "src": "numpy"},
            {"type": "pip", "src": "av"},
            {"type": "pip", "src": "psutil"},
        ],
        "engines": [">=1.1.6"],
        "environment": {"type": "pyenv", "name": "rtc"},
        "titles": {"en": "av.sv", "ko": "av.sv"},
        "descriptions": {"en": "en.sv", "ko": "ko.sv"},
        "documentation_mime": "text",
        "documentations": {},
        "meta": {},
    },
    "controls": {
        "output": [
            {
                "name": "frame",
                "mimes": ["image/jpeg", "image/png"],
            },
        ],
    },
    "props": [
        {
            "rule": "initialize_only",
            "name": "video_src",
            "default_value": "",
            "type": "str",
            "required": True,
            "valid": {},
            "title": {"en": "source"},
            "help": {"en": "address"},
        },
        {
            "rule": "initialize_only",
            "name": "video_index",
            "default_value": 0,
            "type": "int",
            "required": True,
            "valid": {},
            "title": {"ko": "index"},
            "help": {"ko": "number"},
        },
    ],
}


class TemplateTemplateTestCase(TestCase):
    def test_default_v1(self):
        obj = LambdaTemplate()
        obj.deserialize(1, SAMPLE_DATA)

        self.assertEqual(1, obj.version_tuple[0])
        self.assertIsInstance(obj.information, Information)
        self.assertIsInstance(obj.controller, Controller)
        self.assertIsInstance(obj.properties, list)
        self.assertIsNotNone(obj.information)
        self.assertIsNotNone(obj.controller)
        self.assertEqual(2, len(obj.properties))
        for p in obj.properties:
            self.assertIsInstance(p, Property)

        self.assertEqual("av_stream_video", obj.information.name)
        self.assertEqual("1.1.4", obj.information.version)
        self.assertEqual("av", obj.information.category)
        self.assertEqual(["av"], obj.information.keywords)
        self.assertEqual("https://answer.bogonets.com/", obj.information.homepage)
        self.assertEqual("https://answer.bogonets.com/", obj.information.bugs)
        self.assertIsNone(obj.information.license_name)
        self.assertEqual("Bogonet License", obj.information.license_text)
        self.assertEqual("zer0", obj.information.author)
        self.assertEqual(3, len(obj.information.dependencies))
        self.assertEqual("pip", obj.information.dependencies[0].category)
        self.assertEqual("numpy", obj.information.dependencies[0].source)
        self.assertIsNone(obj.information.dependencies[0].destination)
        self.assertIsNone(obj.information.dependencies[0].extra)
        self.assertEqual("pip", obj.information.dependencies[1].category)
        self.assertEqual("av", obj.information.dependencies[1].source)
        self.assertIsNone(obj.information.dependencies[1].destination)
        self.assertIsNone(obj.information.dependencies[1].extra)
        self.assertEqual("pip", obj.information.dependencies[2].category)
        self.assertEqual("psutil", obj.information.dependencies[2].source)
        self.assertIsNone(obj.information.dependencies[2].destination)
        self.assertIsNone(obj.information.dependencies[2].extra)
        self.assertEqual([">=1.1.6"], obj.information.engines)
        self.assertEqual("pyenv", obj.information.environment.category)
        self.assertEqual("rtc", obj.information.environment.name)
        self.assertEqual({"en": "av.sv", "ko": "av.sv"}, obj.information.titles)
        self.assertEqual({"en": "en.sv", "ko": "ko.sv"}, obj.information.descriptions)
        self.assertEqual("text", obj.information.documentation_mime)
        self.assertIsNotNone(obj.information.documentations)
        self.assertEqual(0, len(obj.information.documentations))
        self.assertIsNotNone(obj.information.meta)
        self.assertEqual(0, len(obj.information.meta))

        self.assertIsNone(obj.controller.data_inputs)
        self.assertEqual(1, len(obj.controller.data_outputs))
        self.assertEqual("frame", obj.controller.data_outputs[0].name)
        self.assertEqual(
            ["image/jpeg", "image/png"], obj.controller.data_outputs[0].mimes
        )

        self.assertEqual("video_src", obj.properties[0].name)
        self.assertEqual("initialize_only", obj.properties[0].rule)
        self.assertEqual("", obj.properties[0].value_default)
        self.assertEqual("str", obj.properties[0].value_type)
        self.assertTrue(obj.properties[0].required)
        self.assertEqual(1, len(obj.properties[0].titles))
        self.assertEqual("source", obj.properties[0].titles["en"])
        self.assertEqual(1, len(obj.properties[0].helps))
        self.assertEqual("address", obj.properties[0].helps["en"])

        self.assertEqual("video_index", obj.properties[1].name)
        self.assertEqual("initialize_only", obj.properties[1].rule)
        self.assertEqual(0, obj.properties[1].value_default)
        self.assertEqual("int", obj.properties[1].value_type)
        self.assertTrue(obj.properties[1].required)
        self.assertEqual(1, len(obj.properties[1].titles))
        self.assertEqual("index", obj.properties[1].titles["ko"])
        self.assertEqual(1, len(obj.properties[1].helps))
        self.assertEqual("number", obj.properties[1].helps["ko"])

        serialize_data = obj.serialize(1)
        changed_controls = {
            "output": {
                "dynamic": False,
                "method": "numpy",
                "list": [
                    {
                        "name": "frame",
                        "mimes": ["image/jpeg", "image/png"],
                    },
                ],
            },
        }
        self.assertEqual(changed_controls, serialize_data["controls"])
        self.assertEqual(SAMPLE_DATA["info"], serialize_data["info"])
        self.assertEqual(SAMPLE_DATA["props"], serialize_data["props"])


if __name__ == "__main__":
    main()
