# -*- coding: utf-8 -*-

from unittest import TestCase, main
from typing import Any
from json import loads as json_loads
from recc.serialization.byte import (
    pickling,
    unpickling,
    orjson_encoder,
    orjson_decoder,
    orjson_zlib_encoder,
    orjson_zlib_decoder,
    orjson_gzip_encoder,
    orjson_gzip_decoder,
    orjson_lzma_encoder,
    orjson_lzma_decoder,
    orjson_bz2_encoder,
    orjson_bz2_decoder,
    msgpack_encoder,
    msgpack_decoder,
    msgpack_zlib_encoder,
    msgpack_zlib_decoder,
    msgpack_gzip_encoder,
    msgpack_gzip_decoder,
    msgpack_lzma_encoder,
    msgpack_lzma_decoder,
    msgpack_bz2_encoder,
    msgpack_bz2_decoder,
)
from tester.samples.read_samples import read_sample


def _read_sample_object() -> Any:
    return json_loads(read_sample("set_graph.v1.data.json"))


class SerializeByteTestCase(TestCase):
    def test_pickle(self):
        sample = _read_sample_object()
        serialize_data = pickling(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = unpickling(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_orjson(self):
        sample = _read_sample_object()
        serialize_data = orjson_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = orjson_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_orjson_zlib(self):
        sample = _read_sample_object()
        serialize_data = orjson_zlib_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = orjson_zlib_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_orjson_gzip(self):
        sample = _read_sample_object()
        serialize_data = orjson_gzip_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = orjson_gzip_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_orjson_lzma(self):
        sample = _read_sample_object()
        serialize_data = orjson_lzma_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = orjson_lzma_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_orjson_bz2(self):
        sample = _read_sample_object()
        serialize_data = orjson_bz2_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = orjson_bz2_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_msgpack(self):
        sample = _read_sample_object()
        serialize_data = msgpack_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = msgpack_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_msgpack_zlib(self):
        sample = _read_sample_object()
        serialize_data = msgpack_zlib_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = msgpack_zlib_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_msgpack_gzip(self):
        sample = _read_sample_object()
        serialize_data = msgpack_gzip_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = msgpack_gzip_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_msgpack_lzma(self):
        sample = _read_sample_object()
        serialize_data = msgpack_lzma_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = msgpack_lzma_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)

    def test_msgpack_bz2(self):
        sample = _read_sample_object()
        serialize_data = msgpack_bz2_encoder(sample)
        self.assertLess(0, len(serialize_data))
        deserialize_data = msgpack_bz2_decoder(serialize_data)
        self.assertEqual(sample, deserialize_data)


if __name__ == "__main__":
    main()
