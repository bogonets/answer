# -*- coding: utf-8 -*-

import os
from unittest import IsolatedAsyncioTestCase, main
from tempfile import TemporaryDirectory, NamedTemporaryFile
from recc.aio.file_remover import remove_files_from_subprocess


class DateParseTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        self.root = TemporaryDirectory()
        self.subdir = TemporaryDirectory(dir=self.root.name)

        files = [
            NamedTemporaryFile(dir=self.root.name, delete=False),
            NamedTemporaryFile(dir=self.root.name, delete=False),
            NamedTemporaryFile(dir=self.subdir.name, delete=False),
            NamedTemporaryFile(dir=self.subdir.name, delete=False),
        ]

        for f in files:
            f.write(b"0000")
            f.close()

        self.files = [f.name for f in files]
        self.assertTrue(os.path.isdir(self.root.name))
        self.assertTrue(os.path.isdir(self.subdir.name))
        self.assertTrue(os.path.isfile(self.files[0]))
        self.assertTrue(os.path.isfile(self.files[1]))
        self.assertTrue(os.path.isfile(self.files[2]))
        self.assertTrue(os.path.isfile(self.files[3]))

    def tearDown(self):
        self.root.cleanup()

    async def test_remove_files_from_subprocess(self):
        await remove_files_from_subprocess(
            self.files[0],
            self.subdir.name,
        )

        self.assertTrue(os.path.exists(self.root.name))
        self.assertFalse(os.path.exists(self.subdir.name))
        self.assertFalse(os.path.exists(self.files[0]))
        self.assertTrue(os.path.exists(self.files[1]))
        self.assertFalse(os.path.exists(self.files[2]))
        self.assertFalse(os.path.exists(self.files[3]))


if __name__ == "__main__":
    main()
