# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.driver.xml import (
    global_xml_decoder,
    global_xml_encoder,
    install_xmltodict_driver,
)


class XmlToDictTestCase(TestCase):
    def setUp(self):
        install_xmltodict_driver()

    def test_default(self):
        test = {
            "data": {
                "test1": [1, 2, 3],
                "test2": ["a", "b", "c", "d"],
                "test3": {
                    "a": 1,
                    "b": 2,
                    "c": "3",
                },
            }
        }

        xml_text = global_xml_encoder(test)
        self.assertIsInstance(xml_text, str)

        result = global_xml_decoder(xml_text)
        self.assertEqual(1, int(result["data"]["test1"][0]))
        self.assertEqual(2, int(result["data"]["test1"][1]))
        self.assertEqual(3, int(result["data"]["test1"][2]))

        self.assertEqual("a", result["data"]["test2"][0])
        self.assertEqual("b", result["data"]["test2"][1])
        self.assertEqual("c", result["data"]["test2"][2])
        self.assertEqual("d", result["data"]["test2"][3])

        self.assertEqual(1, int(result["data"]["test3"]["a"]))
        self.assertEqual(2, int(result["data"]["test3"]["b"]))
        self.assertEqual("3", result["data"]["test3"]["c"])


if __name__ == "__main__":
    main()
