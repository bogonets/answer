# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.control import Control


class TemplateControlTestCase(TestCase):
    def test_default(self):
        obj = Control()
        obj.name = "a"
        obj.mimes = ["b", "c"]
        data = obj.__serialize__()
        self.assertEqual("a", data["name"])
        self.assertEqual(2, len(data["mimes"]))
        self.assertEqual("b", data["mimes"][0])
        self.assertEqual("c", data["mimes"][1])

        obj.__deserialize__(data)
        self.assertEqual("a", obj.name)
        self.assertEqual(2, len(obj.mimes))
        self.assertEqual("b", obj.mimes[0])
        self.assertEqual("c", obj.mimes[1])


if __name__ == "__main__":
    main()
