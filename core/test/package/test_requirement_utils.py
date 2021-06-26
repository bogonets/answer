# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.package.requirement_utils import (
    RECC_REQUIREMENTS_MAIN,
    read_requirements_main_from_source_file,
)


class RequirementUtilsTestCase(TestCase):
    def test_requirements(self):
        packages = read_requirements_main_from_source_file()
        self.assertEqual(set(packages), set(RECC_REQUIREMENTS_MAIN))


if __name__ == "__main__":
    main()
