# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.locale import Locale
from recc.template.property import Property


class TemplatePropertyTestCase(TestCase):
    def test_default(self):
        obj = Property()
        obj.titles = Locale()
        obj.choice = ["a", "b"]
        obj.hint = ["c", "d"]
        obj.titles["en"] = "english"
        obj.titles["ko"] = "korean"
        obj.helps = Locale()
        obj.helps["jp"] = "japanese"

        data = obj.__serialize__()
        self.assertIsInstance(data, dict)
        self.assertEqual(["a", "b"], data["choice"])
        self.assertEqual(["c", "d"], data["hint"])
        self.assertEqual(2, len(data["titles"]))
        self.assertEqual("english", data["titles"]["en"])
        self.assertEqual("korean", data["titles"]["ko"])
        self.assertEqual(1, len(data["helps"]))
        self.assertEqual("japanese", data["helps"]["jp"])

        data2 = Property()
        data2.__deserialize__(data)
        self.assertEqual(["a", "b"], data2.choice)
        self.assertEqual(["c", "d"], data2.hint)
        self.assertEqual(2, len(data2.titles))
        self.assertEqual("english", data2.titles["en"])
        self.assertEqual("korean", data2.titles["ko"])
        self.assertEqual(1, len(data2.helps))
        self.assertEqual("japanese", data2.helps["jp"])


if __name__ == "__main__":
    main()
