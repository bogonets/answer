# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.argparse.parser.dict_parse import get_namespace_by_dict


class DictParseTestCase(TestCase):
    def test_default(self):
        data = {"aa": {"bb": {"cc": 100}}}
        config = get_namespace_by_dict(data, "aa", "bb")
        self.assertEqual(100, config.cc)


if __name__ == "__main__":
    main()
