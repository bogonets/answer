# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.template.dependency import Dependency


class TemplateDependencyTestCase(TestCase):
    def test_default_v1(self):
        obj = Dependency()
        obj.category = "pip"
        obj.source = "numpy"
        obj.destination = "localhost"
        obj.extra = ["arg1", "arg2"]
        data = obj.serialize(1)
        self.assertEqual("pip", data["type"])
        self.assertEqual("numpy", data["src"])
        self.assertEqual("localhost", data["dest"])
        self.assertEqual(["arg1", "arg2"], data["extra"])

        obj2 = Dependency()
        obj2.deserialize(1, data)
        self.assertEqual("pip", obj2.category)
        self.assertEqual("numpy", obj2.source)
        self.assertEqual("localhost", obj2.destination)
        self.assertEqual(["arg1", "arg2"], obj2.extra)

    def test_default_v2(self):
        cat = "curl"
        url = "http://localhost:8080/download.zip"
        dest = "/usr/name/Downloads/download.zip"
        args = {"0": "-k", "1": "-v"}

        obj = Dependency()
        obj.category = cat
        obj.source = url
        obj.destination = dest
        obj.extra = args
        data = obj.serialize(2)
        self.assertEqual(cat, data["category"])
        self.assertEqual(url, data["source"])
        self.assertEqual(dest, data["destination"])
        self.assertEqual(args, data["extra"])

        obj2 = Dependency()
        obj2.deserialize(2, data)
        self.assertEqual(cat, obj2.category)
        self.assertEqual(url, obj2.source)
        self.assertEqual(dest, obj2.destination)
        self.assertEqual(args, obj2.extra)


if __name__ == "__main__":
    main()
