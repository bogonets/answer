# -*- coding: utf-8 -*-

from unittest import TestCase, main

from recc.mime.mime_codec_register import get_global_mime_register


class _ComplexObject:
    def __init__(self):
        self.test_data1 = "text"
        self.test_data2 = 100
        self.test_data3 = 3.14


class MimeCodecRegisterTestCase(TestCase):
    def test_binary(self):
        test_data = {"aa": 11, "bb": 22.5, "cc": [1, 2, 3]}
        codec = get_global_mime_register()
        encoded_data = codec.encode_binary(test_data)
        self.assertIsInstance(encoded_data, bytes)
        decoded_data = codec.decode_binary(encoded_data)
        self.assertIsInstance(decoded_data, dict)
        self.assertEqual(decoded_data, test_data)

    def test_binary_complex(self):
        test_data = _ComplexObject()
        codec = get_global_mime_register()
        encoded_data = codec.encode_binary(test_data)
        self.assertIsInstance(encoded_data, bytes)
        decoded_data = codec.decode_binary(encoded_data)
        self.assertIsInstance(decoded_data, _ComplexObject)
        self.assertEqual(decoded_data.test_data1, test_data.test_data1)
        self.assertEqual(decoded_data.test_data2, test_data.test_data2)
        self.assertEqual(decoded_data.test_data3, test_data.test_data3)

    def test_json(self):
        test_data = {"aa": 11, "bb": 22.5, "cc": [1, 2, 3]}
        codec = get_global_mime_register()
        encoded_data = codec.encode_json(test_data)
        self.assertIsInstance(encoded_data, bytes)
        decoded_data = codec.decode_json(encoded_data)
        self.assertIsInstance(decoded_data, dict)
        self.assertEqual(decoded_data, test_data)

    def test_text(self):
        test_data = "Hello, World!"
        codec = get_global_mime_register()
        encoded_data = codec.encode_text(test_data)
        self.assertIsInstance(encoded_data, bytes)
        decoded_data = codec.decode_text(encoded_data)
        self.assertIsInstance(decoded_data, str)
        self.assertEqual(decoded_data, test_data)


if __name__ == "__main__":
    main()
