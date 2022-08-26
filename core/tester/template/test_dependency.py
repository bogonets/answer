# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.dependency import Dependency


class TemplateDependencyTestCase(TestCase):
    def test_default(self):
        cat = "curl"
        url = "http://localhost:8080/download.zip"
        dest = "/usr/name/Downloads/download.zip"
        args = {"0": "-k", "1": "-v"}

        obj = Dependency()
        obj.category = cat
        obj.source = url
        obj.destination = dest
        obj.extra = args
        data = obj.__serialize__()
        self.assertEqual(cat, data["category"])
        self.assertEqual(url, data["source"])
        self.assertEqual(dest, data["destination"])
        self.assertEqual(args, data["extra"])

        obj2 = Dependency()
        obj2.__deserialize__(data)
        self.assertEqual(cat, obj2.category)
        self.assertEqual(url, obj2.source)
        self.assertEqual(dest, obj2.destination)
        self.assertEqual(args, obj2.extra)


if __name__ == "__main__":
    main()
