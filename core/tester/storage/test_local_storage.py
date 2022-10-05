# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main

from recc.storage.local_storage import LocalStorage


class LocalStorageTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        self.local_storage = LocalStorage(self.temp_dir.name)

        self.assertTrue(os.path.isdir(self.local_storage.root))
        self.assertTrue(os.path.isdir(self.local_storage.workspace))

    async def asyncTearDown(self):
        self.temp_dir.cleanup()


if __name__ == "__main__":
    main()
