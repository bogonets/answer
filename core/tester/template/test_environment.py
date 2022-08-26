# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.environment import Environment


class TemplateEnvironmentTestCase(TestCase):
    def test_default(self):
        obj = Environment()
        obj.category = "venv"
        obj.name = "numpy"
        data = obj.__serialize__()
        self.assertEqual("venv", data["category"])
        self.assertEqual("numpy", data["name"])

        obj2 = Environment()
        obj2.__deserialize__(data)
        self.assertEqual("venv", obj2.category)
        self.assertEqual("numpy", obj2.name)


if __name__ == "__main__":
    main()
