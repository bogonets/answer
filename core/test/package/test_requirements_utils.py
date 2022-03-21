# -*- coding: utf-8 -*-

import os
from unittest import TestCase, main
from recc.package.requirements_utils import (
    _RECC_PACKAGE_DIR,  # noqa
    _read_requirements,  # noqa
    RECC_REQUIREMENTS_MAIN,
)


class RequirementsUtilsTestCase(TestCase):
    def test_with_original_requirements(self):
        recc_dir = os.path.dirname(_RECC_PACKAGE_DIR)
        core_dir = os.path.dirname(recc_dir)
        requirements_main_path = os.path.join(core_dir, "requirements.main.txt")
        original_requirements = _read_requirements(requirements_main_path)
        self.assertListEqual(original_requirements, RECC_REQUIREMENTS_MAIN)


if __name__ == "__main__":
    main()
