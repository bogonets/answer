# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.environment import Environment


class TemplateEnvironmentTestCase(TestCase):
    def test_default_v1(self):
        obj = Environment()
        obj.category = "venv"
        obj.name = "numpy"
        data = obj.__serialize__(1)
        self.assertEqual("venv", data["type"])
        self.assertEqual("numpy", data["name"])

        obj2 = Environment()
        obj2.__deserialize__(1, data)
        self.assertEqual("venv", obj2.category)
        self.assertEqual("numpy", obj2.name)

    def test_default_v2(self):
        obj = Environment()
        obj.category = "venv"
        obj.name = "numpy"
        data = obj.__serialize__(2)
        self.assertEqual("venv", data["category"])
        self.assertEqual("numpy", data["name"])

        obj2 = Environment()
        obj2.__deserialize__(2, data)
        self.assertEqual("venv", obj2.category)
        self.assertEqual("numpy", obj2.name)


if __name__ == "__main__":
    main()
