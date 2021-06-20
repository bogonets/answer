# -*- coding: utf-8 -*-

from unittest import TestCase, main
from recc.mime.mime_register import (
    TYPE_APPLICATION,
    TYPE_AUDIO,
    TYPE_FONT,
    TYPE_EXAMPLE,
    TYPE_IMAGE,
    TYPE_MESSAGE,
    TYPE_MODEL,
    TYPE_MULTIPART,
    TYPE_TEXT,
    TYPE_VIDEO,
    REGISTERED_MIMES,
)


class MimeRegisterTestCase(TestCase):
    def test_registered_mimes(self):
        self.assertLess(0, len(REGISTERED_MIMES))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_APPLICATION]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_AUDIO]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_FONT]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_EXAMPLE]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_IMAGE]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_MESSAGE]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_MODEL]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_MULTIPART]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_TEXT]))
        self.assertEqual(0, len(REGISTERED_MIMES[TYPE_VIDEO]))


if __name__ == "__main__":
    main()
