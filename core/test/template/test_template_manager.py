# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.template.template_manager import json_to_py_extension, TemplateManager


class TemplateManagerTestCase(TestCase):
    def test_json_to_py_extension(self):
        test01_origin = "/root/path.app.json/test.app.json"
        test01_actual = json_to_py_extension(test01_origin)
        test01_expect = "/root/path.app.json/test.app.py"
        self.assertEqual(test01_expect, test01_actual)

        test02_origin = "aaa.json"
        test02_actual = json_to_py_extension(test02_origin)
        test02_expect = "aaa.py"
        self.assertEqual(test02_expect, test02_actual)

        test03_origin = "/mmm/aa.json/temp.app"
        test03_actual = json_to_py_extension(test03_origin)
        test03_expect = "/mmm/aa.json/temp.app"
        self.assertEqual(test03_expect, test03_actual)

    def test_default(self):
        mgr = TemplateManager()
        mgr.refresh()
        self.assertLess(0, len(mgr.keys()))


if __name__ == "__main__":
    main()
