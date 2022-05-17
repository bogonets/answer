# -*- coding: utf-8 -*-

import sys
from unittest import TestCase, main

from recc.system.path_context import PathContext


class PathContextTestCase(TestCase):
    def test_append(self):
        original_path_length = len(sys.path)
        with PathContext("/a", "/b") as pc:
            self.assertEqual(original_path_length, len(pc.original_path))
            self.assertListEqual(["/a", "/b"], pc.request_path)
            self.assertFalse(pc.insert_operation)

            changed_path_length = len(sys.path)
            self.assertEqual(original_path_length + 2, changed_path_length)
            self.assertEqual(sys.path[changed_path_length - 1], "/b")
            self.assertEqual(sys.path[changed_path_length - 2], "/a")

    def test_insert(self):
        original_path_length = len(sys.path)
        with PathContext("/a", "/b", insert_operation=True) as pc:
            self.assertEqual(original_path_length, len(pc.original_path))
            self.assertListEqual(["/a", "/b"], pc.request_path)
            self.assertTrue(pc.insert_operation)

            changed_path_length = len(sys.path)
            self.assertEqual(original_path_length + 2, changed_path_length)
            self.assertEqual(sys.path[0], "/b")
            self.assertEqual(sys.path[1], "/a")


if __name__ == "__main__":
    main()
