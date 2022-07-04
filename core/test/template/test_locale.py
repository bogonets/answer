# -*- coding: utf-8 -*-

from typing import Iterable, Mapping, MutableMapping
from unittest import TestCase, main

from recc.template.locale import Locale


class TemplateLocaleTestCase(TestCase):
    def test_type(self):
        self.assertTrue(issubclass(Locale, Iterable))
        self.assertTrue(issubclass(Locale, Mapping))
        self.assertTrue(issubclass(Locale, MutableMapping))

    def test_default_v1(self):
        obj = Locale()
        obj["en"] = "Hah"
        obj["ko"] = "Eng"
        data = obj.__serialize__(1)
        self.assertEqual(2, len(data))
        self.assertEqual("Hah", data["en"])
        self.assertEqual("Eng", data["ko"])

        obj2 = Locale()
        obj2.__deserialize__(1, data)
        self.assertEqual(2, len(obj2))
        self.assertEqual("Hah", obj2["en"])
        self.assertEqual("Eng", obj2["ko"])

    def test_default_v2(self):
        obj = Locale()
        obj["en"] = "Hah"
        obj["ko"] = "Eng"
        data = obj.__serialize__(2)
        self.assertEqual(2, len(data))
        self.assertEqual("Hah", data["en"])
        self.assertEqual("Eng", data["ko"])

        obj2 = Locale()
        obj2.__deserialize__(2, data)
        self.assertEqual(2, len(obj2))
        self.assertEqual("Hah", obj2["en"])
        self.assertEqual("Eng", obj2["ko"])


if __name__ == "__main__":
    main()
