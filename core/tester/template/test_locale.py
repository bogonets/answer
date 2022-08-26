# -*- coding: utf-8 -*-

from typing import Iterable, Mapping, MutableMapping
from unittest import TestCase, main

from recc.template.locale import Locale


class TemplateLocaleTestCase(TestCase):
    def test_type(self):
        self.assertTrue(issubclass(Locale, Iterable))
        self.assertTrue(issubclass(Locale, Mapping))
        self.assertTrue(issubclass(Locale, MutableMapping))

    def test_default(self):
        obj = Locale()
        obj["en"] = "Hah"
        obj["ko"] = "Eng"
        data = obj.__serialize__()
        self.assertEqual(2, len(data))
        self.assertEqual("Hah", data["en"])
        self.assertEqual("Eng", data["ko"])

        obj2 = Locale()
        obj2.__deserialize__(data)
        self.assertEqual(2, len(obj2))
        self.assertEqual("Hah", obj2["en"])
        self.assertEqual("Eng", obj2["ko"])


if __name__ == "__main__":
    main()
