# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from recc.translations.translator import Translator

EN_JSON = """
{
    "f1": {
        "s1": {
            "t1": "en-f1-s1-t1"
        }
    }
}
"""

KO_JSON = """
{
    "f1": {
        "s1": {
            "t1": "ko-f1-s1-t1"
        }
    }
}
"""


class JsonTranslatorTestCase(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()

        en_json = os.path.join(self.temp.name, "en.json")
        with open(en_json, "w") as f1:
            f1.write(EN_JSON)

        ko_json = os.path.join(self.temp.name, "ko.json")
        with open(ko_json, "w") as f2:
            f2.write(KO_JSON)

    def tearDown(self):
        self.temp.cleanup()

    def test_default(self):
        trans = Translator.from_dir(self.temp.name, "en")
        self.assertEqual("en-f1-s1-t1", trans.t("f1.s1.t1"))

        trans.lang = "ko"
        self.assertEqual("ko-f1-s1-t1", trans.t("f1.s1.t1"))


if __name__ == "__main__":
    main()
