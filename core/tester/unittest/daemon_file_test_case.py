# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase
from recc.variables.storage import LOCAL_STORAGE_DAEMON_NAME
from tester.plugins.copy_plugin import copy_plugin


class DaemonFileTestCase(IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.daemon_dir = os.path.join(self.temp.name, LOCAL_STORAGE_DAEMON_NAME)
        os.mkdir(self.daemon_dir)
        self.daemon_filename = "daemon_simple.py"
        self.daemon_path = copy_plugin(self.daemon_filename, self.daemon_dir)
        self.assertTrue(os.path.isfile(self.daemon_path))

    def tearDown(self):
        self.temp.cleanup()
