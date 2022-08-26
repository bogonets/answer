# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main
from recc.venv.pyvenv_cfg import read_pyvenv_cfg, read_site_packages_dir

_SAMPLE_PYENV_CFG = """home = /unknown/venv/root
include-system-site-packages = true
version = 3.7.3
"""


class PyvenvCfgTestCase(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.pyenv_cfg_path = os.path.join(self.temp_dir.name, "pyvenv.cfg")
        with open(self.pyenv_cfg_path, "w") as f:
            f.write(_SAMPLE_PYENV_CFG)
        self.assertTrue(os.path.isfile(self.pyenv_cfg_path))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_read_pyvenv_cfg(self):
        cfg = read_pyvenv_cfg(self.temp_dir.name)
        self.assertEqual("/unknown/venv/root", cfg.home)
        self.assertTrue(cfg.include_system_site_packages)
        self.assertEqual("3.7.3", cfg.version)

    def test_read_site_packages_dir(self):
        path = read_site_packages_dir(self.temp_dir.name)
        self.assertTrue(path.endswith("lib/python3.7/site-packages"))


if __name__ == "__main__":
    main()
