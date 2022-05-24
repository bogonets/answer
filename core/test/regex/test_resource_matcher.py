# -*- coding: utf-8 -*-

import os
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from recc.regex.resource_matcher import MatchItem, find_match_file


class ResourceMatcherTestCase(TestCase):
    def test_parse_and_match(self):
        m1 = MatchItem.parse((r"(.*)", r"\1"))
        self.assertEqual("a", m1.match("a", lambda x: True))

        m2 = MatchItem.parse((r"%(.*)=(.*)%", r"\2,\1"))
        self.assertEqual("b,a", m2.match("%a=b%", lambda x: True))

        m3 = MatchItem.parse("index.html")
        self.assertEqual("index.html", m3.match("b", lambda x: True))

        m4 = MatchItem.parse(("Unknown",))
        self.assertEqual("Unknown", m4.match("c", lambda x: True))

        m5 = MatchItem.parse((r"index\.html", "index.html"))
        self.assertEqual("index.html", m5.match("index.html", lambda x: True))
        self.assertIsNone(m5.match("index@html", lambda x: True))

    def test_find_match_file(self):
        with TemporaryDirectory() as tmpdir:
            index_html = os.path.join(tmpdir, "index.html")
            with open(index_html, "w") as f1:
                f1.write("\n")

            index_css = os.path.join(tmpdir, "index.css")
            with open(index_css, "w") as f2:
                f2.write("\n")

            self.assertTrue(os.path.isfile(index_html))
            self.assertTrue(os.path.isfile(index_css))

            m1 = MatchItem.parse((r"(.*)", r"\1"))
            m2 = MatchItem.parse("index.html")
            matches = [m1, m2]

            r1 = find_match_file(matches, "index.css", tmpdir)
            self.assertEqual("index.css", r1)

            r2 = find_match_file(matches, "index.js", tmpdir)
            self.assertEqual("index.html", r2)

            r3 = find_match_file(matches, "index.html", tmpdir)
            self.assertEqual("index.html", r3)


if __name__ == "__main__":
    main()
