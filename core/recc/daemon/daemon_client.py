# -*- coding: utf-8 -*-

import grpc
from typing import Optional
from uuid import uuid4
from grpc.aio._channel import Channel  # noqa
from recc.chrono.datetime import today
from recc.logging.logging import recc_daemon_logger as logger
from recc.serialization.byte_coding import ByteCodingType
from recc.daemon.daemon_answer import DaemonAnswer
from recc.daemon.packet.content_packer import ContentPacker
from recc.daemon.packet.content_unpacker import content_unpack
from recc.memory.shared_memory_queue import SharedMemoryQueue
from recc.memory.shared_memory_validator import (
    SharedMemoryTestInfo,
    register_shared_memory,
)
from recc.serialization.byte import COMPRESS_LEVEL_BEST
from recc.proto.daemon.daemon_api_pb2_grpc import DaemonApiStub
from recc.proto.daemon.daemon_api_pb2 import (
    Pit,
    Pat,
    RegisterCode,
    RegisterQ,
    RegisterA,
    PacketQ,
    PacketA,
)
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


class DaemonClient:

    _session: str
    _channel: Optional[Channel] = None
    _stub: Optional[DaemonApiStub] = None
    _is_sm: Optional[bool] = None

    def __init__(
        self,
        address: str,
        timeout: Optional[float] = None,
        disable_shared_memory=False,
        verbose=False,
    ):
        self._session = uuid4().hex
        self._address = address
        self._options = dict()
        if timeout is not None:
            self._options["timeout"] = timeout
        self._smq = SharedMemoryQueue()
        self._encoding = DEFAULT_PICKLE_ENCODING
        self._compress_level = COMPRESS_LEVEL_BEST
        self._coding = ByteCodingType.MsgpackZlib
        self._min_sm_size = 0
        self._min_sm_byte = 0

        self.disable_shared_memory = disable_shared_memory
        self.verbose = verbose

    def __repr__(self) -> str:
        return f"DaemonClient<{self._address}>"

    def __str__(self) -> str:
        return f"DaemonClient<{self._address}>"

    @property
    def address(self) -> str:
        return self._address

    def is_open(self) -> bool:
        return self._channel is not None

    @property
    def possible_shared_memory(self) -> bool:
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

    async def register(self, *args: str, **kwargs: str) -> int:
        assert self._stub is not None

        with register_shared_memory(self.disable_shared_memory) as test:
            assert isinstance(test, SharedMemoryTestInfo)
            request = RegisterQ(
                session=self._session,
                args=args,
                kwargs=kwargs,
                test_sm_name=test.name,
                test_sm_pass=test.data,
            )
            response = await self._stub.Register(request, **self._options)

        assert isinstance(response, RegisterA)
        self._is_sm = response.is_sm

        if response.min_sm_size > self._min_sm_size:
            self._min_sm_size = response.min_sm_size
        if response.min_sm_byte > self._min_sm_byte:
            self._min_sm_byte = response.min_sm_byte

        if response.code == RegisterCode.Success:
            pass
        elif response.code == RegisterCode.NotFoundRegisterFunction:
            logger.warning("Not found register function")
        else:
            logger.error(f"Unknown register code: {response.code}")
        return response.code

    async def request(self, method: str, path: str, *args, **kwargs) -> DaemonAnswer:
        assert self._stub is not None

        coding = self._coding
        encoding = self._encoding
        compress_level = self._compress_level

        use_sm = self.possible_shared_memory and not self.disable_shared_memory
        smq: Optional[SharedMemoryQueue]
        if use_sm:
            min_sm_size = self._min_sm_size
            min_sm_byte = self._min_sm_byte
            smq = self._smq
        else:
            min_sm_size = 0
            min_sm_byte = 0
            smq = None

        renter = self._smq.multi_rent(min_sm_size, min_sm_byte)
        with renter as sms:
            packer = ContentPacker(
                coding=coding,
                compress_level=compress_level,
                args=args,
                kwargs=kwargs,
                smq=smq,
            )

            packer_begin = today()
            with packer as contents:
                if self.verbose:
                    packer_seconds = (today() - packer_begin).total_seconds()
                    packer_elapsed = round(packer_seconds, 3)
                    logger.debug(f"Packer[sm={use_sm}]: {packer_elapsed}s")

                packet = PacketQ(
                    session=self._session,
                    method=method if method else str(),
                    path=path if path else str(),
                    coding=int(coding.value),  # type: ignore[arg-type]
                    args=contents.args,
                    kwargs=contents.kwargs,
                    sm_names=sms.keys(),
                )

                handshake_begin = today()
                response = await self._stub.Packet(packet, **self._options)
                if self.verbose:
                    handshake_seconds = (today() - handshake_begin).total_seconds()
                    handshake_elapsed = round(handshake_seconds, 3)
                    logger.debug(f"Handshake[sm={use_sm}]: {handshake_elapsed}s")

            assert isinstance(response, PacketA)
            unpacker_begin = today()
            result = content_unpack(
                coding=coding,
                encoding=encoding,
                args=response.args,
                kwargs=response.kwargs,
                sms=sms,
            )
            if self.verbose:
                unpacker_seconds = (today() - unpacker_begin).total_seconds()
                unpacker_elapsed = round(unpacker_seconds, 3)
                logger.debug(f"Unpacker[sm={use_sm}]: {unpacker_elapsed}s")

            return result

    async def get(self, path: str, *args, **kwargs):
        return await self.request(M_GET, path, *args, **kwargs)

    async def head(self, path: str, *args, **kwargs):
        return await self.request(M_HEAD, path, *args, **kwargs)

    async def post(self, path: str, *args, **kwargs):
        return await self.request(M_POST, path, *args, **kwargs)

    async def put(self, path: str, *args, **kwargs):
        return await self.request(M_PUT, path, *args, **kwargs)

    async def delete(self, path: str, *args, **kwargs):
        return await self.request(M_DELETE, path, *args, **kwargs)

    async def connect(self, path: str, *args, **kwargs):
        return await self.request(M_CONNECT, path, *args, **kwargs)

    async def options(self, path: str, *args, **kwargs):
        return await self.request(M_OPTIONS, path, *args, **kwargs)

    async def trace(self, path: str, *args, **kwargs):
        return await self.request(M_TRACE, path, *args, **kwargs)

    async def patch(self, path: str, *args, **kwargs):
        return await self.request(M_PATCH, path, *args, **kwargs)


def create_daemon_client(address: str, timeout: Optional[float] = None) -> DaemonClient:
    return DaemonClient(address, timeout)
