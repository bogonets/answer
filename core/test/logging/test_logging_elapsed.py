# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase, TestCase, main
from logging import DEBUG, WARNING, StreamHandler, getLogger
from io import StringIO
from time import sleep
from recc.logging.logging_elapsed import logging_elapsed


class AsyncLoggingElapsedTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.name = "test.recc.logging.elapsed.async"
        self.buffer = StringIO()
        self.logger = getLogger(self.name)
        self.logger.addHandler(StreamHandler(self.buffer))
        self.logger.setLevel(DEBUG)

    async def asyncTearDown(self):
        self.buffer.close()

    async def test_logging_elapsed(self):
        @logging_elapsed(self.logger, DEBUG)
        async def _test() -> None:
            sleep(0.1)

        await _test()
        self.assertTrue(self.buffer.getvalue())


class LoggingElapsedTestCase(TestCase):
    def setUp(self):
        self.name = "test.recc.logging.elapsed"
        self.buffer = StringIO()
        self.logger = getLogger(self.name)
        self.logger.addHandler(StreamHandler(self.buffer))
        self.logger.setLevel(WARNING)

    def tearDown(self):
        self.buffer.close()

    def test_logging_elapsed(self):
        @logging_elapsed(self.logger, WARNING)
        def _test() -> None:
            sleep(0.1)

        _test()
        self.assertTrue(self.buffer.getvalue())


if __name__ == "__main__":
    main()
