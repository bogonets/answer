# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.template.manager.lamda_template_position import (
    LamdaTemplatePosition,
    LAMDA_TEMPLATE_POSITION_MAP,
)


class LamdaTemplatePositionTestCase(TestCase):
    def test_enum_map(self):
        enum_map = LAMDA_TEMPLATE_POSITION_MAP
        self.assertTrue(3, len(enum_map))

        self.assertTrue(LamdaTemplatePosition.Builtin, enum_map["Builtin"])
        self.assertTrue(LamdaTemplatePosition.Package, enum_map["Package"])
        self.assertTrue(LamdaTemplatePosition.Storage, enum_map["Storage"])

        self.assertRaises(KeyError, lambda: enum_map["builtin"])
        self.assertRaises(KeyError, lambda: enum_map["package"])
        self.assertRaises(KeyError, lambda: enum_map["storage"])


if __name__ == "__main__":
    main()
