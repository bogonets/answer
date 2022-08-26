# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.template.information import Information


class TemplateInformationTestCase(TestCase):
    def test_default(self):
        obj = Information()
        obj.name = "lambda"
        obj.license_name = "mit"
        obj.license_text = "..."
        data = obj.__serialize__()
        self.assertIsInstance(data, dict)
        self.assertEqual(3, len(data))
        self.assertEqual("lambda", data["name"])
        self.assertEqual("mit", data["license_name"])
        self.assertEqual("...", data["license_text"])

        obj2 = Information()
        obj2.__deserialize__(data)
        self.assertEqual("lambda", obj2.name)
        self.assertEqual("mit", obj2.license_name)
        self.assertEqual("...", obj2.license_text)


if __name__ == "__main__":
    main()
