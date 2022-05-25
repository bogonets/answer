# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from recc.translations.translator import Translator

SINGLE_YAML = """
en:
    f1:
        s1: "en-f1-s1"

ko:
    f1:
        s1: "ko-f1-s1"
"""


class YamlSingleTranslatorTestCase(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.single_yaml = os.path.join(self.temp.name, "single.yaml")
        with open(self.single_yaml, "w") as f2:
            f2.write(SINGLE_YAML)

    def tearDown(self):
        self.temp.cleanup()

    def test_default(self):
        trans = Translator.from_file(self.single_yaml, "en")
        self.assertEqual("en-f1-s1", trans.t("f1.s1"))

        trans.lang = "ko"
        self.assertEqual("ko-f1-s1", trans.t("f1.s1"))

        with self.assertRaises(KeyError):
            trans.t("f2")


if __name__ == "__main__":
    main()
