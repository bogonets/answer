# -*- coding: utf-8 -*-

import grpc
import pickle
from typing import Optional, Any, Mapping, Text, Tuple
from grpc.aio._channel import Channel  # noqa
from recc.mime.mime_codec_register import MimeCodecRegister, get_global_mime_register
from recc.network.uds import is_uds_family
from recc.proto.daemon.daemon_api_pb2_grpc import DaemonApiStub
from recc.proto.daemon.daemon_api_pb2 import Pit, Pat, InitQ, InitA, PacketQ, PacketA
from recc.variables.rpc import (
    DEFAULT_GRPC_OPTIONS,
    DEFAULT_PICKLE_PROTOCOL_VERSION,
    DEFAULT_PICKLE_ENCODING,
    DEFAULT_HEARTBEAT_TIMEOUT,
)

_WELL_KNOWN_LOOPBACK_ADDRESSES = [
    "127.0.0.1",
    "localhost",
]


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

    def is_localhost(self) -> bool:
        if is_uds_family(self._address):
            return True

        # elif self._address.startswith("ipv4:"):
        #     pass
        # elif self._address.startswith("ipv6:"):
        #     pass
        # elif self._address.startswith("dns:"):
        #     # TODO: Remove `//authority/` part.
        #     pass
        # else:
        #     # If unknown, use `dns` scheme.
        #     pass

        # TODO: Find IPv4 loopback address (127.0.0.0/8)
        # TODO: Find IPv6 loopback address (::1, [::1])
        # TODO: Find `localhost` in /etc/hosts
        # TODO: Find `localhost` in C:\Windows\System32\drivers\etc\hosts
        # TODO: Find network address
        # TODO: E.T.C ...

        return self._address.split(":")[0] in _WELL_KNOWN_LOOPBACK_ADDRESSES

    def is_possible_shared_memory(self) -> bool:
        return self.is_localhost()

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

    async def init(self, *args, **kwargs) -> int:
        assert self._stub is not None
        updated_args = [str(a) for a in args]
        updated_kwargs = {str(k): str(v) for k, v in kwargs.items()}
        request = InitQ(args=updated_args, kwargs=updated_kwargs)
        response = await self._stub.Init(request, **self._options)
        assert isinstance(response, InitA)
        return response.code

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
