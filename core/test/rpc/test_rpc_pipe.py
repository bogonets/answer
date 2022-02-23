# -*- coding: utf-8 -*-

import os
from json import loads as json_loads
from typing import Any, Callable
from datetime import datetime
from dataclasses import dataclass
from tempfile import TemporaryDirectory
from unittest import IsolatedAsyncioTestCase, main, skipIf
from recc.argparse.default_namespace import get_default_task_config
from recc.rpc.rpc_client import create_rpc_client
from recc.task.task_server import create_task_server
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
from tester.variables import (
    GRPC_PACKET_PERFORMANCE_TEST_SKIP,
    GRPC_PACKET_PERFORMANCE_ITERATION,
    GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE,
)

ByteEncoder = Callable[[Any], bytes]
ByteDecoder = Callable[[bytes], Any]


def _read_sample_object() -> Any:
    return json_loads(read_sample("set_graph.v1.data.json"))


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
        self.temp = TemporaryDirectory()
        self.assertTrue(os.path.isdir(self.temp.name))

        address = "unix://" + os.path.join(self.temp.name, "sock.pip")
        config = get_default_task_config()
        config.task_workspace_dir = self.temp.name
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
        self.assertFalse(self.client.is_open())

        self.assertTrue(os.path.isdir(self.temp.name))
        self.temp.cleanup()
        self.assertFalse(os.path.isdir(self.temp.name))

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
            _read_sample_object(),
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

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_pickle_echo_data(self):
        message = await self._default_performance_echo_data(pickling, unpickling)
        print(f"Pickle {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_orjson_byte_echo_data(self):
        message = await self._default_performance_echo_data(
            orjson_encoder, orjson_decoder
        )
        print(f"Orjson {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_orjson_zlib_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_zlib_encoder(x, 1),
            orjson_zlib_decoder,
        )
        print(f"Orjson+zlib(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_orjson_zlib_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_zlib_encoder(x, 9),
            orjson_zlib_decoder,
        )
        print(f"Orjson+zlib(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_orjson_gzip_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_gzip_encoder(x, 1),
            orjson_gzip_decoder,
        )
        print(f"Orjson+gzip(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_orjson_gzip_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_gzip_encoder(x, 9),
            orjson_gzip_decoder,
        )
        print(f"Orjson+gzip(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_orjson_bz2_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_bz2_encoder(x, 1),
            orjson_bz2_decoder,
        )
        print(f"Orjson+bz2(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_orjson_bz2_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: orjson_bz2_encoder(x, 9),
            orjson_bz2_decoder,
        )
        print(f"Orjson+bz2(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_orjson_lzma_echo_data(self):
        message = await self._default_performance_echo_data(
            orjson_lzma_encoder,
            orjson_lzma_decoder,
        )
        print(f"Orjson+lzma {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_msgpack_byte_echo_data(self):
        message = await self._default_performance_echo_data(
            msgpack_encoder, msgpack_decoder
        )
        print(f"Msgpack {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_msgpack_zlib_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: msgpack_zlib_encoder(x, 1),
            msgpack_zlib_decoder,
        )
        print(f"Msgpack+zlib(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_msgpack_zlib_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: msgpack_zlib_encoder(x, 9),
            msgpack_zlib_decoder,
        )
        print(f"Msgpack+zlib(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_msgpack_gzip_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: msgpack_gzip_encoder(x, 1),
            msgpack_gzip_decoder,
        )
        print(f"Msgpack+gzip(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_msgpack_gzip_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: msgpack_gzip_encoder(x, 9),
            msgpack_gzip_decoder,
        )
        print(f"Msgpack+gzip(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_msgpack_bz2_level1_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: msgpack_bz2_encoder(x, 1),
            msgpack_bz2_decoder,
        )
        print(f"Msgpack+bz2(level=1) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_msgpack_bz2_level9_echo_data(self):
        message = await self._default_performance_echo_data(
            lambda x: msgpack_bz2_encoder(x, 9),
            msgpack_bz2_decoder,
        )
        print(f"Msgpack+bz2(level=9) {message}")

    @skipIf(GRPC_PACKET_PERFORMANCE_TEST_SKIP, GRPC_PACKET_PERFORMANCE_SKIP_MESSAGE)
    async def test_msgpack_lzma_echo_data(self):
        message = await self._default_performance_echo_data(
            msgpack_lzma_encoder,
            msgpack_lzma_decoder,
        )
        print(f"Msgpack+lzma {message}")


if __name__ == "__main__":
    main()
