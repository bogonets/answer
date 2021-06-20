# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.exception.recc_error import (
    CODE_RECC_OK,
    RECC_CODE_TO_ERROR_TYPE_MAP,
)


class ReccErrorTestCase(TestCase):
    def test_code_to_error(self):
        self.assertIn(CODE_RECC_OK, RECC_CODE_TO_ERROR_TYPE_MAP.keys())


if __name__ == "__main__":
    main()
