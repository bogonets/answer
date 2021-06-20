# -*- coding: utf-8 -*-

import unittest
from recc.http.http_client import normalize_url_path


class HttpClientTestCase(unittest.TestCase):
    def test_normalize_url_path(self):
        self.assertEqual("/", normalize_url_path(""))
        self.assertEqual("/", normalize_url_path("/"))
        self.assertEqual("/a", normalize_url_path("a"))
        self.assertEqual("/a", normalize_url_path("/a"))
        self.assertEqual("/aaa", normalize_url_path("aaa"))
        self.assertEqual("/aaa", normalize_url_path("/aaa"))


if __name__ == "__main__":
    unittest.main()
