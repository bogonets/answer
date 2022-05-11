# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main
from recc.package.requirements_utils import (
    _RECC_PACKAGE_DIR,  # noqa
    read_packages,
    RECC_REQUIREMENTS_MAIN,
)


class RequirementsUtilsTestCase(TestCase):
    def test_with_original_requirements(self):
        recc_dir = os.path.dirname(_RECC_PACKAGE_DIR)
        core_dir = os.path.dirname(recc_dir)
        requirements_main_path = os.path.join(core_dir, "requirements.main.txt")
        self.assertTrue(os.path.isfile(requirements_main_path))

        original_requirements = read_packages(requirements_main_path)
        self.assertListEqual(original_requirements, RECC_REQUIREMENTS_MAIN)


if __name__ == "__main__":
    main()
