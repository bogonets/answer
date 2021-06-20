# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.mime.mime_type import (
    MimeType,
    MIME_ANY,
    MIME_ANY_BOTH,
    MIME_APPLICATION_OCTET_STREAM,
    MIME_APPLICATION_JSON,
    MIME_TEXT_PLAIN,
)


class MimeTypeTestCase(TestCase):
    def test_default(self):
        self.assertEqual("application", MIME_APPLICATION_OCTET_STREAM.family)
        self.assertEqual("octet-stream", MIME_APPLICATION_OCTET_STREAM.subtype)

        self.assertEqual("application", MIME_APPLICATION_JSON.family)
        self.assertEqual("json", MIME_APPLICATION_JSON.subtype)

        self.assertEqual("text", MIME_TEXT_PLAIN.family)
        self.assertEqual("plain", MIME_TEXT_PLAIN.subtype)

    def test_test_accept(self):
        text_any = MimeType.parse("text/*")
        any_plain = MimeType.parse("*/plain")
        self.assertTrue(MIME_TEXT_PLAIN.test_from_accepts([text_any]))
        self.assertTrue(MIME_TEXT_PLAIN.test_from_accepts([any_plain]))
        self.assertTrue(MIME_TEXT_PLAIN.test_from_accepts([MIME_ANY]))
        self.assertTrue(MIME_TEXT_PLAIN.test_from_accepts([MIME_ANY_BOTH]))

        text_unknown = MimeType.parse("text/unknown")
        unknown_text = MimeType.parse("unknown/text")
        error_mimes = [text_unknown, text_unknown]
        self.assertFalse(MIME_TEXT_PLAIN.test_from_accepts([text_unknown]))
        self.assertFalse(MIME_TEXT_PLAIN.test_from_accepts([unknown_text]))
        self.assertFalse(MIME_TEXT_PLAIN.test_from_accepts(error_mimes))

        mixed_mimes = [text_unknown, text_unknown, MIME_ANY]
        self.assertTrue(MIME_TEXT_PLAIN.test_from_accepts(mixed_mimes))


if __name__ == "__main__":
    main()
