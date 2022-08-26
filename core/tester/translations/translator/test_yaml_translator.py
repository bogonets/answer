# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from recc.translations.translator import Translator

EN_YAML = """
f1:
    s1: "en-f1-s1"
    s2: "en-f1-s2"

f2:
    s1: "en-f2-s1"
    s2: "en-f2-s2"

f3:
    s1:
        t1: "en-f3-s1-t1"

f4: "a-{arg}-b"
"""

KO_YAML = """
f1:
    s1: "ko-f1-s1"
    s2: "ko-f1-s2"

f2:
    s1: "ko-f2-s1"
    s2: "ko-f2-s2"
"""


class YamlTranslatorTestCase(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()

        en_yaml = os.path.join(self.temp.name, "en.yaml")
        with open(en_yaml, "w") as f1:
            f1.write(EN_YAML)

        ko_yaml = os.path.join(self.temp.name, "ko.yaml")
        with open(ko_yaml, "w") as f2:
            f2.write(KO_YAML)

    def tearDown(self):
        self.temp.cleanup()

    def test_default(self):
        trans = Translator.from_dir(self.temp.name, "en")
        self.assertEqual("en-f1-s1", trans.t("f1.s1"))
        self.assertEqual("en-f1-s2", trans.t("f1.s2"))
        self.assertEqual("en-f2-s1", trans.t("f2.s1"))
        self.assertEqual("en-f2-s2", trans.t("f2.s2"))

        trans.lang = "ko"
        self.assertEqual("ko-f1-s1", trans.t("f1.s1"))
        self.assertEqual("ko-f1-s2", trans.t("f1.s2"))
        self.assertEqual("ko-f2-s1", trans.t("f2.s1"))
        self.assertEqual("ko-f2-s2", trans.t("f2.s2"))

        # Fallback
        self.assertEqual("en-f3-s1-t1", trans.t("f3.s1.t1"))
        self.assertEqual("a-K-b", trans.t("f4", arg="K"))


if __name__ == "__main__":
    main()
