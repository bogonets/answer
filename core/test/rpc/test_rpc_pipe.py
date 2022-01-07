# -*- coding: utf-8 -*-

import os
import pickle
import orjson
import zlib
import gzip
import lzma
import bz2
from typing import Any, Callable
from datetime import datetime
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main, skipIf
from recc.argparse.default_namespace import get_default_task_config
from recc.rpc.rpc_client import create_rpc_client
from recc.task.task_server import create_task_server
from recc.variables.rpc import (
    DEFAULT_PICKLE_PROTOCOL_VERSION,
    DEFAULT_PICKLE_ENCODING,
)
from tester.samples.read_samples import read_sample
from tester.variables import (
    GRPC_PACKET_PERFORMANCE_TEST_SKIP,
    GRPC_PACKET_PERFORMANCE_ITERATION,
)

ByteEncoder = Callable[[Any], bytes]
ByteDecoder = Callable[[bytes], Any]


def pickling(data: Any) -> bytes:
    return pickle.dumps(data, protocol=DEFAULT_PICKLE_PROTOCOL_VERSION)


def unpickling(data: bytes) -> Any:
    return pickle.loads(data, encoding=DEFAULT_PICKLE_ENCODING)


def orjson_byte_encoder(data: Any) -> bytes:
    return orjson.dumps(data)


def orjson_byte_decoder(data: bytes) -> Any:
    return orjson.loads(data)


def orjson_byte_zlib_encoder(data: Any, level: int = 1) -> bytes:
    assert level == -1 or 0 <= level <= 9
    return zlib.compress(orjson.dumps(data), level=level)


def orjson_byte_zlib_decoder(data: bytes) -> Any:
    return orjson.loads(zlib.decompress(data))


def orjson_byte_gzip_encoder(data: Any, level: int = 1) -> bytes:
    assert 0 <= level <= 9
    return gzip.compress(orjson.dumps(data), compresslevel=level)


def orjson_byte_gzip_decoder(data: bytes) -> Any:
    return orjson.loads(gzip.decompress(data))


def orjson_byte_lzma_encoder(data: Any) -> bytes:
    return lzma.compress(orjson.dumps(data))


def orjson_byte_lzma_decoder(data: bytes) -> Any:
    return orjson.loads(lzma.decompress(data))


def orjson_byte_bz2_encoder(data: Any, level: int = 1) -> bytes:
    assert 1 <= level <= 9
    return bz2.compress(orjson.dumps(data), compresslevel=level)


def orjson_byte_bz2_decoder(data: bytes) -> Any:
    return orjson.loads(bz2.decompress(data))


def read_sample_object() -> Any:
    return orjson.loads(read_sample("set_graph.v1.data.json"))


@dataclass
class _Result:
    count: int
    total_bytes: int
    total_encoding_seconds: float
    total_handshake_seconds: float
    total_decoding_seconds: float

    @property
    def average_bytes(self) -> float:
        return round(self.total_bytes / self.count, 2)

    @property
    def total_seconds(self) -> float:
        tes = self.total_encoding_seconds
        ths = self.total_handshake_seconds
        tds = self.total_decoding_seconds
        return tes + ths + tds

    @property
    def average_seconds(self) -> float:
        return self.total_seconds / self.count

    @property
    def average_encoding_seconds(self) -> float:
        return self.total_encoding_seconds / self.count

    @property
    def average_handshake_seconds(self) -> float:
        return self.total_handshake_seconds / self.count

    @property
    def average_decoding_seconds(self) -> float:
        return self.total_decoding_seconds / self.count


@skipIf(os.name != "posix", "It only runs on posix")
class RpcPipeClientTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = TemporaryDirectory()
        address = "unix://" + os.path.join(self.temp_dir.name, "sock.pip")

        config = get_default_task_config()
        config.task_address = address
        server_info = create_task_server(config)
        self.server = server_info.server
        self.client = create_rpc_client(address)

        await self.server.start()
        await self.client.open()
        self.assertTrue(self.client.is_open())

    async def asyncTearDown(self):
        await self.client.close()
        await self.server.stop(None)
        self.temp_dir.cleanup()
        self.assertFalse(self.client.is_open())

    async def test_heartbeat(self):
        self.assertTrue(await self.client.heartbeat(0))

    async def _performance_echo_data(
        self,
        sample_data: Any,
        count: int,
        encoder: ByteEncoder,
        decoder: ByteDecoder,
    ) -> _Result:
        total_bytes = 0
        total_encoding_seconds = 0.0
        total_handshake_seconds = 0.0
        total_decoding_seconds = 0.0

        for n in range(count):
            encoding_begin = datetime.now()
            send_data = encoder(sample_data)
            encoding_seconds = (datetime.now() - encoding_begin).total_seconds()
            total_encoding_seconds += encoding_seconds
            total_bytes += len(send_data)

            handshake_begin = datetime.now()
            recv_data = await self.client.echo_data(send_data)
            handshake_seconds = (datetime.now() - handshake_begin).total_seconds()
            total_handshake_seconds += handshake_seconds

            decoding_begin = datetime.now()
            decoded_data = decoder(recv_data)
            decoding_seconds = (datetime.now() - decoding_begin).total_seconds()
            total_decoding_seconds += decoding_seconds

            self.assertEqual(recv_data, send_data)
            self.assertEqual(decoded_data, sample_data)

        return _Result(
            count,
            total_bytes,
            total_encoding_seconds,
            total_handshake_seconds,
            total_decoding_seconds,
        )

    async def _default_performance_echo_data(
        self, encoder: ByteEncoder, decoder: ByteDecoder
    ) -> str:
        result = await self._performance_echo_data(
            read_sample_object(),
            GRPC_PACKET_PERFORMANCE_ITERATION,
            encoder,
            decoder,
        )
        count = result.count
        time = result.total_seconds
        size = result.average_bytes
        return (
            f"grpc-pipe echo-data {count} iteration "
            f"{time:.4f}s ({size:,} byte/packet)"
        )

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_pickle_echo_data(self):
        message = await self._default_performance_echo_data(pickling, unpickling)
        print(f"Pickle {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_orjson_byte_echo_data(self):
        message = await self._default_performance_echo_data(
            orjson_byte_encoder, orjson_byte_decoder
        )
        print(f"Orjson {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_orjson_byte_zlib_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_byte_zlib_encoder(x, 1),
            orjson_byte_zlib_decoder,
        )
        print(f"Orjson+zlib(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_orjson_byte_zlib_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_byte_zlib_encoder(x, 9),
            orjson_byte_zlib_decoder,
        )
        print(f"Orjson+zlib(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_orjson_byte_gzip_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_byte_gzip_encoder(x, 1),
            orjson_byte_gzip_decoder,
        )
        print(f"Orjson+gzip(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_orjson_byte_gzip_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_byte_gzip_encoder(x, 9),
            orjson_byte_gzip_decoder,
        )
        print(f"Orjson+gzip(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_orjson_byte_bz2_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_byte_bz2_encoder(x, 1),
            orjson_byte_bz2_decoder,
        )
        print(f"Orjson+bz2(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_orjson_byte_bz2_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_byte_bz2_encoder(x, 9),
            orjson_byte_bz2_decoder,
        )
        print(f"Orjson+bz2(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, "GRPC Packet performance testing is off")
    async def test_orjson_byte_lzma_echo_data(self):
        message = await self._default_performance_echo_data(
            orjson_byte_lzma_encoder,
            orjson_byte_lzma_decoder,
        )
        print(f"Orjson+lzma {message}")


if __name__ == "__main__":
    main()
