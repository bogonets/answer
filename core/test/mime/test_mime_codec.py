# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.mime.mime_codec import MimeCodec


class MimeCodecTestCase(TestCase):
    def test_default(self):
        codec = MimeCodec("unknown/text")
        self.assertEqual("unknown/text", codec.mime.mime)


if __name__ == "__main__":
    main()
