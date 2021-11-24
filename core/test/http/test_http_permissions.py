# -*- coding: utf-8 -*-

from unittest import main, TestCase
from recc.http.http_permissions import (
    has_group_graph_read,
    has_project_setting_read,
    has_project_setting_write,
    has_features,
    has_administrator,
)
from recc.access_control.policy import Policy
from recc.variables.annotation import (
    ANNOTATION_GROUP_PERMISSIONS,
    ANNOTATION_PROJECT_PERMISSIONS,
    ANNOTATION_FEATURE_PERMISSIONS,
    ANNOTATION_ADMIN_PERMISSION,
)


@has_group_graph_read
def _test1():
    pass


@has_project_setting_read
@has_project_setting_write
def _test2():
    pass


@has_features("f1", "f2")
def _test3():
    pass


@has_administrator
def _test4():
    pass


class HttpPermissionsTestCase(TestCase):
    def test_group(self):
        self.assertFalse(hasattr(_test1, ANNOTATION_PROJECT_PERMISSIONS))
        self.assertFalse(hasattr(_test1, ANNOTATION_FEATURE_PERMISSIONS))
        self.assertFalse(hasattr(_test1, ANNOTATION_ADMIN_PERMISSION))

        test1 = getattr(_test1, ANNOTATION_GROUP_PERMISSIONS)
        self.assertIsInstance(test1, list)
        self.assertEqual(1, len(test1))
        self.assertIn(Policy.HasGraphRead, test1)

    def test_project(self):
        self.assertFalse(hasattr(_test2, ANNOTATION_GROUP_PERMISSIONS))
        self.assertFalse(hasattr(_test2, ANNOTATION_FEATURE_PERMISSIONS))
        self.assertFalse(hasattr(_test2, ANNOTATION_ADMIN_PERMISSION))

        test2 = getattr(_test2, ANNOTATION_PROJECT_PERMISSIONS)
        self.assertIsInstance(test2, list)
        self.assertEqual(2, len(test2))
        self.assertIn(Policy.HasSettingRead, test2)
        self.assertIn(Policy.HasSettingWrite, test2)

    def test_features(self):
        self.assertFalse(hasattr(_test3, ANNOTATION_GROUP_PERMISSIONS))
        self.assertFalse(hasattr(_test3, ANNOTATION_PROJECT_PERMISSIONS))
        self.assertFalse(hasattr(_test3, ANNOTATION_ADMIN_PERMISSION))

        test3 = getattr(_test3, ANNOTATION_FEATURE_PERMISSIONS)
        self.assertIsInstance(test3, list)
        self.assertEqual(2, len(test3))
        self.assertIn("f1", test3)
        self.assertIn("f2", test3)

    def test_admin(self):
        self.assertFalse(hasattr(_test4, ANNOTATION_GROUP_PERMISSIONS))
        self.assertFalse(hasattr(_test4, ANNOTATION_PROJECT_PERMISSIONS))
        self.assertFalse(hasattr(_test4, ANNOTATION_FEATURE_PERMISSIONS))

        test4 = getattr(_test4, ANNOTATION_ADMIN_PERMISSION)
        self.assertIsInstance(test4, bool)
        self.assertTrue(test4)


if __name__ == "__main__":
    main()
