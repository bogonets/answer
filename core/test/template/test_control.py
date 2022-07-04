# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.control import Control


class TemplateControlTestCase(TestCase):
    def test_default_v1(self):
        obj = Control()
        obj.name = "a"
        obj.mimes = ["b", "c"]
        data = obj.__serialize__(1)
        self.assertEqual("a", data["name"])
        self.assertEqual(2, len(data["mimes"]))
        self.assertEqual("b", data["mimes"][0])
        self.assertEqual("c", data["mimes"][1])

        obj.__deserialize__(1, data)
        self.assertEqual("a", obj.name)
        self.assertEqual(2, len(obj.mimes))
        self.assertEqual("b", obj.mimes[0])
        self.assertEqual("c", obj.mimes[1])

    def test_simple_name_v1(self):
        obj = Control()
        obj.__deserialize__(1, "test")
        self.assertEqual("test", obj.name)

    def test_simple_mimes_v1(self):
        obj = Control()
        obj.__deserialize__(1, {"mimes": "a"})
        self.assertEqual(1, len(obj.mimes))
        self.assertEqual("a", obj.mimes[0])

    def test_default_v2(self):
        obj = Control()
        obj.name = "a"
        obj.mimes = ["b", "c"]
        data = obj.__serialize__(2)
        self.assertEqual("a", data["name"])
        self.assertEqual(2, len(data["mimes"]))
        self.assertEqual("b", data["mimes"][0])
        self.assertEqual("c", data["mimes"][1])

        obj.__deserialize__(2, data)
        self.assertEqual("a", obj.name)
        self.assertEqual(2, len(obj.mimes))
        self.assertEqual("b", obj.mimes[0])
        self.assertEqual("c", obj.mimes[1])


if __name__ == "__main__":
    main()
