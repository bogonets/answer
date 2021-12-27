# -*- coding: utf-8 -*-

from unittest import main, TestCase
from recc.http.http_decorator import (
    has_graph_view,
    has_setting_view,
    has_setting_edit,
)
from recc.variables.annotation import ANNOTATION_PERMISSIONS
from recc.variables.database import (
    PERMISSION_SLUG_RECC_DOMAIN_GRAPH_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
)


@has_graph_view
def _test1():
    pass


@has_setting_view
@has_setting_edit
def _test2():
    pass


class HttpDecoratorTestCase(TestCase):
    def test_default_1(self):
        test1 = getattr(_test1, ANNOTATION_PERMISSIONS)
        self.assertIsInstance(test1, list)
        self.assertEqual(1, len(test1))
        self.assertIn(PERMISSION_SLUG_RECC_DOMAIN_GRAPH_VIEW, test1)

    def test_default_2(self):
        test2 = getattr(_test2, ANNOTATION_PERMISSIONS)
        self.assertIsInstance(test2, list)
        self.assertEqual(2, len(test2))
        self.assertIn(PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW, test2)
        self.assertIn(PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT, test2)


if __name__ == "__main__":
    main()
