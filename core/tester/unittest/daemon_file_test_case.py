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

        self.requirements1_path = os.path.join(self.daemon_dir, "requirements.txt")
        self.requirements2_path = os.path.join(self.daemon_dir, "requirements2.txt")
        with open(self.requirements1_path, "w") as r1:
            r1.write("numpy")
        with open(self.requirements2_path, "w") as r2:
            r2.write("numpy")
        self.assertTrue(os.path.isfile(self.requirements1_path))
        self.assertTrue(os.path.isfile(self.requirements2_path))

        self.constraints1_path = os.path.join(self.daemon_dir, "constraints.txt")
        self.constraints2_path = os.path.join(self.daemon_dir, "constraints2.txt")
        with open(self.constraints1_path, "w") as c1:
            c1.write("numpy")
        with open(self.constraints2_path, "w") as c2:
            c2.write("numpy")
        self.assertTrue(os.path.isfile(self.constraints1_path))
        self.assertTrue(os.path.isfile(self.constraints2_path))

    def tearDown(self):
        self.temp.cleanup()
