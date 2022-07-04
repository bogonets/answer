# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.information import Information


class TemplateInformationTestCase(TestCase):
    def test_default_v1(self):
        data = {
            "name": "av_stream_video",
            "version": "1.1.4",
            "category": "av",
            "keywords": "av",
            "homepage": "https://answer.bogonets.com/",
            "bugs": "https://answer.bogonets.com/",
            "license": "Bogonet License",
            "author": "zer0",
            "dependencies": [
                {"type": "pip", "src": "numpy"},
                {"type": "pip", "src": "av"},
                {"type": "pip", "src": "psutil"},
            ],
            "engines": ">=1.1.6",
            "environment": {"type": "pyenv", "name": "rtc"},
            "titles": {"en": "av.sv", "ko": "av.sv"},
            "descriptions": {"en": "en.sv", "ko": "ko.sv"},
            "documentation_mime": "text",
            "documentations": {},
            "meta": {},
        }

        obj = Information()
        obj.__deserialize__(1, data)
        self.assertEqual("av_stream_video", obj.name)
        self.assertEqual("1.1.4", obj.version)
        self.assertEqual("av", obj.category)
        self.assertEqual(["av"], obj.keywords)
        self.assertEqual("https://answer.bogonets.com/", obj.homepage)
        self.assertEqual("https://answer.bogonets.com/", obj.bugs)
        self.assertIsNone(obj.license_name)
        self.assertEqual("Bogonet License", obj.license_text)
        self.assertEqual("zer0", obj.author)
        self.assertEqual(3, len(obj.dependencies))
        self.assertEqual("pip", obj.dependencies[0].category)
        self.assertEqual("numpy", obj.dependencies[0].source)
        self.assertIsNone(obj.dependencies[0].destination)
        self.assertIsNone(obj.dependencies[0].extra)
        self.assertEqual("pip", obj.dependencies[1].category)
        self.assertEqual("av", obj.dependencies[1].source)
        self.assertIsNone(obj.dependencies[1].destination)
        self.assertIsNone(obj.dependencies[1].extra)
        self.assertEqual("pip", obj.dependencies[2].category)
        self.assertEqual("psutil", obj.dependencies[2].source)
        self.assertIsNone(obj.dependencies[2].destination)
        self.assertIsNone(obj.dependencies[2].extra)
        self.assertEqual([">=1.1.6"], obj.engines)
        self.assertEqual("pyenv", obj.environment.category)
        self.assertEqual("rtc", obj.environment.name)
        self.assertEqual({"en": "av.sv", "ko": "av.sv"}, obj.titles)
        self.assertEqual({"en": "en.sv", "ko": "ko.sv"}, obj.descriptions)
        self.assertEqual("text", obj.documentation_mime)
        self.assertIsNotNone(obj.documentations)
        self.assertEqual(0, len(obj.documentations))
        self.assertIsNotNone(obj.meta)
        self.assertEqual(0, len(obj.meta))

        serialize_data = obj.__serialize__(1)
        self.assertIsInstance(serialize_data, dict)
        self.assertIsInstance(serialize_data["keywords"], list)
        self.assertEqual(1, len(serialize_data["keywords"]))
        self.assertEqual("av", serialize_data["keywords"][0])
        serialize_data["keywords"] = data["keywords"]

        self.assertIsInstance(serialize_data["engines"], list)
        self.assertEqual(1, len(serialize_data["engines"]))
        self.assertEqual(">=1.1.6", serialize_data["engines"][0])
        serialize_data["engines"] = data["engines"]

        self.assertEqual(data, serialize_data)

    def test_default_v2(self):
        obj = Information()
        obj.name = "lambda"
        obj.license_name = "mit"
        obj.license_text = "..."
        data = obj.__serialize__(2)
        self.assertIsInstance(data, dict)
        self.assertEqual(3, len(data))
        self.assertEqual("lambda", data["name"])
        self.assertEqual("mit", data["license_name"])
        self.assertEqual("...", data["license_text"])

        obj2 = Information()
        obj2.__deserialize__(2, data)
        self.assertEqual("lambda", obj2.name)
        self.assertEqual("mit", obj2.license_name)
        self.assertEqual("...", obj2.license_text)


if __name__ == "__main__":
    main()
