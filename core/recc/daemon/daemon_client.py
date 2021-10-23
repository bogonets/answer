# -*- coding: utf-8 -*-

import grpc
import pickle
from typing import Optional, Any, Mapping, Text, Tuple
from grpc.aio._channel import Channel  # noqa
from recc.mime.mime_codec_register import MimeCodecRegister, get_global_mime_register
from recc.proto.daemon.daemon_api_pb2_grpc import DaemonApiStub
from recc.proto.daemon.daemon_api_pb2 import Pit, Pat, PacketQ, PacketA
from recc.variables.rpc import (
    DEFAULT_GRPC_OPTIONS,
    DEFAULT_PICKLE_PROTOCOL_VERSION,
    DEFAULT_PICKLE_ENCODING,
    DEFAULT_HEARTBEAT_TIMEOUT,
)


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

    _channel: Optional[Channel] = None
    _stub: Optional[DaemonApiStub] = None

    def __init__(
        self,
        address: str,
        timeout: Optional[float] = None,
        mimes: Optional[MimeCodecRegister] = None,
    ):
        self._address = address
        self._options = dict()
        if timeout is not None:
            self._options["timeout"] = timeout
        self._pickling_protocol_version = DEFAULT_PICKLE_PROTOCOL_VERSION
        self._unpickling_encoding = DEFAULT_PICKLE_ENCODING
        self._mimes = mimes if mimes else get_global_mime_register()

    def __repr__(self) -> str:
        return f"DaemonClient<{self._address}>"

    def __str__(self) -> str:
        return f"DaemonClient<{self._address}>"

    def is_open(self) -> bool:
        return self._channel is not None

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

    def _pickling(self, data: Any) -> bytes:
        return pickle.dumps(data, protocol=self._pickling_protocol_version)

    def _unpickling(self, data: bytes) -> Any:
        return pickle.loads(data, encoding=self._unpickling_encoding)

    async def heartbeat(self, delay: float = 0) -> bool:
        assert self._stub is not None
        response = await self._stub.Heartbeat(Pit(delay=delay), **self._options)
        assert isinstance(response, Pat)
        return response.ok

    async def packet(
        self,
        method: int,
        headers: Optional[Mapping[Text, Text]] = None,
        content: Optional[bytes] = None,
    ) -> Tuple[int, Mapping[Text, Text], Optional[bytes]]:
        assert self._stub is not None
        packet_content = content if content else bytes()
        packet = PacketQ(method=method, headers=headers, content=packet_content)
        response = await self._stub.Packet(packet, **self._options)
        assert isinstance(response, PacketA)
        return response.code, response.headers, response.content

    async def pickling(
        self,
        method: int,
        headers: Optional[Mapping[Text, Text]] = None,
        content: Any = None,
    ) -> Tuple[int, Mapping[Text, Text], Any]:
        assert self._stub is not None
        encoded_content = self._pickling(content)
        request = PacketQ(method=method, headers=headers, content=encoded_content)
        response = await self._stub.Pickling(request, **self._options)
        assert isinstance(response, PacketA)
        decoded_content = self._unpickling(response.content)
        return response.code, response.headers, decoded_content


def create_daemon_client(address: str, timeout: Optional[float] = None) -> DaemonClient:
    return DaemonClient(address, timeout)
