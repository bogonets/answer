# -*- coding: utf-8 -*-

import os
from tempfile import mkstemp, mkdtemp
from unittest import TestCase, main
from recc.filesystem.permission import (
    change_readable,
    change_writable,
    change_executable,
    exists,
    remove_file,
    remove_dir,
    is_readable_file,
    is_writable_file,
    is_executable_file,
    is_readable_dir,
    is_writable_dir,
    is_executable_dir,
)


def _create_temp_file() -> str:
    fd, name = mkstemp()
    os.close(fd)
    return name


def _create_temp_dir() -> str:
    return mkdtemp()


class PermissionTestCase(TestCase):
    def test_readable_file(self):
        path = _create_temp_file()
        change_readable(path)
        self.assertTrue(exists(path))
        self.assertTrue(is_readable_file(path))
        self.assertFalse(is_writable_file(path))
        self.assertFalse(is_executable_file(path))
        self.assertFalse(is_readable_dir(path))
        self.assertFalse(is_writable_dir(path))
        self.assertFalse(is_executable_dir(path))
        remove_file(path)

    def test_writable_file(self):
        path = _create_temp_file()
        change_writable(path)
        self.assertTrue(exists(path))
        self.assertFalse(is_readable_file(path))
        self.assertTrue(is_writable_file(path))
        self.assertFalse(is_executable_file(path))
        self.assertFalse(is_readable_dir(path))
        self.assertFalse(is_writable_dir(path))
        self.assertFalse(is_executable_dir(path))
        remove_file(path)

    def test_executable_file(self):
        path = _create_temp_file()
        change_executable(path)
        self.assertTrue(exists(path))
        self.assertFalse(is_readable_file(path))
        self.assertFalse(is_writable_file(path))
        self.assertTrue(is_executable_file(path))
        self.assertFalse(is_readable_dir(path))
        self.assertFalse(is_writable_dir(path))
        self.assertFalse(is_executable_dir(path))
        remove_file(path)

    def test_readable_dir(self):
        path = _create_temp_dir()
        change_readable(path)
        self.assertTrue(exists(path))
        self.assertFalse(is_readable_file(path))
        self.assertFalse(is_writable_file(path))
        self.assertFalse(is_executable_file(path))
        self.assertTrue(is_readable_dir(path))
        self.assertFalse(is_writable_dir(path))
        self.assertFalse(is_executable_dir(path))
        remove_dir(path)

    def test_writable_dir(self):
        path = _create_temp_dir()
        change_writable(path)
        self.assertTrue(exists(path))
        self.assertFalse(is_readable_file(path))
        self.assertFalse(is_writable_file(path))
        self.assertFalse(is_executable_file(path))
        self.assertFalse(is_readable_dir(path))
        self.assertTrue(is_writable_dir(path))
        self.assertFalse(is_executable_dir(path))
        remove_dir(path)

    def test_executable_dir(self):
        path = _create_temp_dir()
        change_executable(path)
        self.assertTrue(exists(path))
        self.assertFalse(is_readable_file(path))
        self.assertFalse(is_writable_file(path))
        self.assertFalse(is_executable_file(path))
        self.assertFalse(is_readable_dir(path))
        self.assertFalse(is_writable_dir(path))
        self.assertTrue(is_executable_dir(path))
        remove_dir(path)


if __name__ == "__main__":
    main()
