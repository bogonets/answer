# -*- coding: utf-8 -*-

import grpc
from typing import Optional, List, Dict, Any
from uuid import uuid4
from multiprocessing.shared_memory import SharedMemory
from grpc.aio._channel import Channel  # noqa
from recc.daemon.mixin.daemon_packer import DaemonPacker
from recc.daemon.daemon_content_type import DaemonContentType
from recc.memory.shared_memory_queue import SharedMemoryQueue
from recc.serialization.byte import COMPRESS_LEVEL_BEST
from recc.proto.daemon.daemon_api_pb2_grpc import DaemonApiStub
from recc.proto.daemon.daemon_api_pb2 import Pit, Pat, InitQ, InitA, PacketQ, PacketA
from recc.variables.rpc import (
    DEFAULT_GRPC_OPTIONS,
    DEFAULT_HEARTBEAT_TIMEOUT,
    DEFAULT_PICKLE_ENCODING,
)

M_GET = "GET"
M_HEAD = "HEAD"
M_POST = "POST"
M_PUT = "PUT"
M_DELETE = "DELETE"
M_CONNECT = "CONNECT"
M_OPTIONS = "OPTIONS"
M_TRACE = "TRACE"
M_PATCH = "PATCH"


async def heartbeat(
    address: str,
    delay: float = 0,
    timeout: Optional[float] = DEFAULT_HEARTBEAT_TIMEOUT,
) -> bool:
    async with grpc.aio.insecure_channel(
        address, options=DEFAULT_GRPC_OPTIONS
    ) as channel:
        # grpc.channel_ready_future(channel)
        stub = DaemonApiStub(channel)
        options = dict()
        if timeout is not None:
            options["timeout"] = timeout
        response = await stub.Heartbeat(Pit(delay=delay), **options)
    return response.ok


class DaemonClient(DaemonPacker):

    _channel: Optional[Channel] = None
    _stub: Optional[DaemonApiStub] = None
    _is_sm: Optional[bool] = None

    def __init__(
        self,
        address: str,
        timeout: Optional[float] = None,
        disable_shared_memory=False,
    ):
        self._address = address
        self._options = dict()
        if timeout is not None:
            self._options["timeout"] = timeout
        self._disable_shared_memory = disable_shared_memory
        self._smq = SharedMemoryQueue()
        self._encoding = DEFAULT_PICKLE_ENCODING
        self._compress_level = COMPRESS_LEVEL_BEST
        self._content_type = DaemonContentType.MsgpackZlib

    def __repr__(self) -> str:
        return f"DaemonClient<{self._address}>"

    def __str__(self) -> str:
        return f"DaemonClient<{self._address}>"

    @property
    def address(self) -> str:
        return self._address

    def is_open(self) -> bool:
        return self._channel is not None

    def is_possible_shared_memory(self) -> bool:
        return bool(self._is_sm)

    async def open(self) -> None:
        self._channel = grpc.aio.insecure_channel(
            self._address, options=DEFAULT_GRPC_OPTIONS
        )
        self._stub = DaemonApiStub(self._channel)
        await self._channel.channel_ready()

    async def close(self) -> None:
        assert self._channel is not None
        assert self._stub is not None
        await self._channel.close()
        self._channel = None
        self._stub = None

    async def heartbeat(self, delay: float = 0) -> bool:
        assert self._stub is not None
        response = await self._stub.Heartbeat(Pit(delay=delay), **self._options)
        assert isinstance(response, Pat)
        return response.ok

    async def init(
        self,
        args: Optional[List[str]] = None,
        kwargs: Optional[Dict[str, str]] = None,
        configs: Optional[Dict[str, str]] = None,
    ) -> int:
        assert self._stub is not None

        sm: Optional[SharedMemory]
        if self._disable_shared_memory:
            test_sm_pass = str()
            test_sm_pass_bytes = bytes()
            sm = None
            test_sm_name = str()
        else:
            test_sm_pass = uuid4().hex
            test_sm_pass_bytes = bytes.fromhex(test_sm_pass)
            sm = SharedMemory(create=True, size=len(test_sm_pass_bytes))
            test_sm_name = sm.name

        try:
            if sm:
                sm.buf[:] = test_sm_pass_bytes
            request = InitQ(
                args=args if args else list(),
                kwargs=kwargs if kwargs else dict(),
                configs=configs if configs else dict(),
                test_sm_name=test_sm_name,
                test_sm_pass=test_sm_pass,
            )
            response = await self._stub.Init(request, **self._options)
        finally:
            if sm:
                sm.close()
                sm.unlink()

        assert isinstance(response, InitA)
        self._is_sm = response.is_sm
        return response.code

    async def packet(
        self,
        content_type: DaemonContentType,
        method: Optional[str] = None,
        path: Optional[str] = None,
        content: Optional[bytes] = None,
    ) -> bytes:
        assert self._stub is not None

        if content:
            if self._is_sm:
                use_sm = True
                sm_name = self._smq.write(content)
                packet_content = bytes()
                packet_content_size = len(content)
            else:
                use_sm = False
                sm_name = str()
                packet_content = content
                packet_content_size = len(content)
        else:
            use_sm = False
            sm_name = str()
            packet_content = bytes()
            packet_content_size = 0

        packet = PacketQ(
            method=method if method else str(),
            path=path if path else str(),
            sm_name=sm_name,
            content_type=int(content_type.value),  # type: ignore[arg-type]
            content_size=packet_content_size,
            content=packet_content,
        )

        try:
            response = await self._stub.Packet(packet, **self._options)
            assert isinstance(response, PacketA)
            response_size = response.content_size
            if use_sm and not response.content and response_size > 0:
                assert sm_name
                return bytes(self._smq.get_working(sm_name).buf[:response_size])
            else:
                return response.content
        finally:
            if use_sm:
                assert self._is_sm
                assert sm_name
                self._smq.restore(sm_name)

    async def request(
        self,
        method: str,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        content_type = self._content_type
        level = self._compress_level
        encoding = self._encoding

        if data is not None:
            body = self.encode(data, content_type, level=level)
        else:
            body = bytes()

        result = await self.packet(content_type, method, path, body)

        if result:
            return self.decode(result, content_type, cls, encoding=encoding)
        else:
            return result

    async def get(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_GET, path, data, cls)

    async def head(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_HEAD, path, data, cls)

    async def post(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_POST, path, data, cls)

    async def put(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_PUT, path, data, cls)

    async def delete(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_DELETE, path, data, cls)

    async def connect(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_CONNECT, path, data, cls)

    async def options(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_OPTIONS, path, data, cls)

    async def trace(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_TRACE, path, data, cls)

    async def patch(
        self,
        path: str,
        data: Optional[Any] = None,
        cls: Optional[Any] = None,
    ) -> Any:
        return await self.request(M_PATCH, path, data, cls)


def create_daemon_client(address: str, timeout: Optional[float] = None) -> DaemonClient:
    return DaemonClient(address, timeout)
