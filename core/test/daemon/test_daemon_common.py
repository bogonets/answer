# -*- coding: utf-8 -*-

from unittest import main
from tester.unittest.daemon_test_case import DaemonTestCase


class DaemonCommonTestCase(DaemonTestCase):
    async def test_heartbeat(self):
        self.assertTrue(await self.client.heartbeat(0))

    async def test_packet(self):
        test_method = 100
        test_headers = {"key": "val"}
        test_content = b"ABC"
        result = await self.client.packet(test_method, test_headers, test_content)
        self.assertEqual(test_method, result[0])
        self.assertEqual(test_headers, result[1])
        self.assertEqual(test_content, result[2])

    async def test_pickling(self):
        test_method = 1000
        test_headers = {"key1": "val1"}
        test_content = {"A": "1", "B": 100}
        result = await self.client.pickling(test_method, test_headers, test_content)
        self.assertEqual(test_method, result[0])
        self.assertEqual(test_headers, result[1])
        self.assertEqual(test_content, result[2])


if __name__ == "__main__":
    main()
