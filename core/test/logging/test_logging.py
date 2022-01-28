# -*- coding: utf-8 -*-

from unittest import TestCase, main
from logging import DEBUG, INFO, WARNING
from recc.logging.logging import recc_core_logger, recc_http_logger, recc_rpc_logger


class LoggingTestCase(TestCase):
    def test_logging(self):
        recc_core_logger.setLevel("DEBUG")
        recc_http_logger.setLevel("INFO")
        recc_rpc_logger.setLevel("WARNING")

        self.assertEqual(DEBUG, recc_core_logger.level)
        self.assertEqual(INFO, recc_http_logger.level)
        self.assertEqual(WARNING, recc_rpc_logger.level)

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

        recc_rpc_logger.debug("debug")
        recc_rpc_logger.info("info")
        recc_rpc_logger.warning("warning")
        recc_rpc_logger.error("error")
        recc_rpc_logger.critical("critical")


if __name__ == "__main__":
    main()
