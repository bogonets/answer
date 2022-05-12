# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.locale import Locale
from recc.template.property import Property


class TemplatePropertyTestCase(TestCase):
    def test_default_v1(self):
        data = {
            "rule": "initialize_only",
            "name": "options",
            "default_value": "rtsp,tcp",
            "type": "csv",
            "required": False,
            "valid": {
                "advance": True,
                "hint": "rtsp_transport=tcp;rtsp_transport=udp",
                "list": "bgr24;rgb24",
            },
            "title": {"en": "options", "ko": "options"},
            "help": {"en": "en.options", "ko": "ko.options"},
        }
        obj = Property()
        obj.deserialize(1, data)
        self.assertEqual("initialize_only", obj.rule)
        self.assertEqual("options", obj.name)
        self.assertEqual("rtsp,tcp", obj.value_default)
        self.assertEqual("csv", obj.value_type)
        self.assertFalse(obj.required)
        self.assertTrue(obj.advance)
        self.assertEqual(["bgr24", "rgb24"], obj.choice)
        self.assertEqual(["rtsp_transport=tcp", "rtsp_transport=udp"], obj.hint)
        self.assertEqual({"en": "options", "ko": "options"}, obj.titles)
        self.assertEqual({"en": "en.options", "ko": "ko.options"}, obj.helps)

        serialize_data = obj.serialize(1)
        self.assertEqual(data, serialize_data)

    def test_default_v2(self):
        obj = Property()
        obj.titles = Locale()
        obj.choice = ["a", "b"]
        obj.hint = ["c", "d"]
        obj.titles["en"] = "english"
        obj.titles["ko"] = "korean"
        obj.helps = Locale()
        obj.helps["jp"] = "japanese"

        data = obj.serialize(2)
        self.assertIsInstance(data, dict)
        self.assertEqual(["a", "b"], data["choice"])
        self.assertEqual(["c", "d"], data["hint"])
        self.assertEqual(2, len(data["titles"]))
        self.assertEqual("english", data["titles"]["en"])
        self.assertEqual("korean", data["titles"]["ko"])
        self.assertEqual(1, len(data["helps"]))
        self.assertEqual("japanese", data["helps"]["jp"])

        data2 = Property()
        data2.deserialize(2, data)
        self.assertEqual(["a", "b"], data2.choice)
        self.assertEqual(["c", "d"], data2.hint)
        self.assertEqual(2, len(data2.titles))
        self.assertEqual("english", data2.titles["en"])
        self.assertEqual("korean", data2.titles["ko"])
        self.assertEqual(1, len(data2.helps))
        self.assertEqual("japanese", data2.helps["jp"])


if __name__ == "__main__":
    main()
