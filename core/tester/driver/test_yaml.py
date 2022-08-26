# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.driver.yaml import (
    global_yaml_decoder,
    global_yaml_encoder,
    install_pyyaml_driver,
)


class XmlToDictTestCase(TestCase):
    def setUp(self):
        install_pyyaml_driver()

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

        yaml_text = global_yaml_encoder(test)
        self.assertIsInstance(yaml_text, str)

        result = global_yaml_decoder(yaml_text)
        self.assertEqual(result, test)


if __name__ == "__main__":
    main()
