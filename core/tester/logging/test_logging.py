# -*- coding: utf-8 -*-

from logging import DEBUG, INFO
from unittest import TestCase, main

from recc.logging.logging import recc_core_logger, recc_http_logger


class LoggingTestCase(TestCase):
    def test_logging(self):
        recc_core_logger.setLevel("DEBUG")
        recc_http_logger.setLevel("INFO")

        self.assertEqual(DEBUG, recc_core_logger.level)
        self.assertEqual(INFO, recc_http_logger.level)

        recc_core_logger.debug("debug")
        recc_core_logger.info("info")
        recc_core_logger.warning("warning")
        recc_core_logger.error("error")
        recc_core_logger.critical("critical")

        recc_http_logger.debug("debug")
        recc_http_logger.info("info")
        recc_http_logger.warning("warning")
        recc_http_logger.error("error")
        recc_http_logger.critical("critical")


if __name__ == "__main__":
    main()
