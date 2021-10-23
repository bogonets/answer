# -*- coding: utf-8 -*-

import grpc
import pickle
from typing import Optional, List, Any
from grpc.aio._channel import Channel  # noqa
from recc.mime.mime_codec_register import MimeCodecRegister, get_global_mime_register
from recc.serialization.json import serialize_json_text
from recc.blueprint.blueprint import BpTask
from recc.variables.rpc import DEFAULT_GRPC_OPTIONS, DEFAULT_HEARTBEAT_TIMEOUT
from recc.vs.box import BoxData, BoxRequest
from recc.rpc.rpc_converter import (
    cvt_box_datas,
    cvt_node_slot_data_requests,
    cvt_node_slot_datas,
)
from recc.proto.rpc.rpc_api_pb2_grpc import RpcApiStub
from recc.proto.rpc.rpc_api_pb2 import (
    Pit,
    Pat,
    Ping,
    Pong,
    Empty,
    Data,
    Result,
    Names,
    TarFile,
    UploadTemplateQ,
    UploadTemplateA,
    SetTaskBlueprintQ,
    SetTaskBlueprintA,
    NodePropertyPath,
    GetNodePropertyQ,
    GetNodePropertyA,
    SetNodePropertyQ,
    SetNodePropertyA,
    SendSignalQ,
    SendSignalA,
)


# def generate_test_q():
#     for i in range(10):
#         yield api.TestQ(msg=f"Q[{i}]")
#
#
# async def guide_list(stub: RpcApiStub) -> None:
#     async for response in stub.ServerStreamingTest(api.TestQ(msg="Q")):
#         print(f"SS -> TestA({response.msg})")
#
#
# async def guide_route_chat(stub: RpcApiStub) -> None:
#     async for response in stub.BidirectionalStreamingTest(generate_test_q()):
#         print(f"BS -> {response.msg}")
#
#
# async def test_node_client(address=DEFAULT_NODE_ADDRESS) -> None:
#     async with grpc.aio.insecure_channel(address) as channel:
#         stub = RpcApiStub(channel)
#         response = await stub.Test(api.TestQ(msg="Hello Node !"))
#         print(f"TestA({response.msg})")
#
#         response = await stub.ClientStreamingTest(generate_test_q())
#         print(f"CS -> TestA({response.msg})")
#
#         await guide_list(stub)
#         await guide_route_chat(stub)


async def heartbeat(
    address: str,
    delay: float = 0,
    timeout: Optional[float] = DEFAULT_HEARTBEAT_TIMEOUT,
) -> bool:
    async with grpc.aio.insecure_channel(
        address, options=DEFAULT_GRPC_OPTIONS
    ) as channel:
        # grpc.channel_ready_future(channel)
        stub = RpcApiStub(channel)
        options = dict()
        if timeout is not None:
            options["timeout"] = timeout
        response = await stub.Heartbeat(Pit(delay=delay), **options)
    return response.ok


class RpcClient:

    _channel: Optional[Channel] = None
    _stub: Optional[RpcApiStub] = None

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
        self._pickling_protocol_version = 5
        self._unpickling_encoding = "latin1"
        self._mimes = mimes if mimes else get_global_mime_register()

    def __repr__(self) -> str:
        return f"RpcClient<{self._address}>"

    def __str__(self) -> str:
        return f"RpcClient<{self._address}>"

    def is_open(self) -> bool:
        return self._channel is not None

    async def open(self) -> None:
        self._channel = grpc.aio.insecure_channel(
            self._address, options=DEFAULT_GRPC_OPTIONS
        )
        self._stub = RpcApiStub(self._channel)
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

    async def echo(self, msg: str) -> str:
        assert self._stub is not None
        response = await self._stub.Echo(Ping(msg=msg), **self._options)
        assert isinstance(response, Pong)
        return response.msg

    async def echo_data(self, data: bytes) -> bytes:
        assert self._stub is not None
        response = await self._stub.EchoData(Data(data=data), **self._options)
        assert isinstance(response, Data)
        return response.data

    async def get_workspace_subdir(self) -> List[str]:
        assert self._stub is not None
        response = await self._stub.GetWorkspaceSubdir(Empty(), **self._options)
        assert isinstance(response, Names)
        return [str(name) for name in response.names]

    async def get_template_names(self) -> List[str]:
        assert self._stub is not None
        response = await self._stub.GetTemplateNames(Empty(), **self._options)
        assert isinstance(response, Names)
        return [str(name) for name in response.names]

    async def upload_templates(self, data: bytes) -> None:
        assert self._stub is not None
        request = UploadTemplateQ(tar=TarFile(data=data))
        response = await self._stub.UploadTemplate(request, **self._options)
        assert isinstance(response, UploadTemplateA)
        assert isinstance(response.result, Result)

    async def set_task_blueprint_json(self, task_json: str) -> None:
        assert self._stub is not None
        request = SetTaskBlueprintQ(json=task_json)
        response = await self._stub.SetTaskBlueprint(request, **self._options)
        assert isinstance(response, SetTaskBlueprintA)
        assert isinstance(response.result, Result)

    async def set_task_blueprint(self, task: BpTask, version=1) -> None:
        task_json = serialize_json_text(version, task)
        await self.set_task_blueprint_json(task_json)

    async def get_node_property(self, node: str, prop: str) -> Any:
        assert self._stub is not None
        path = NodePropertyPath(node=node, prop=prop)
        request = GetNodePropertyQ(path=path)
        response = await self._stub.GetNodeProperty(request, **self._options)
        assert isinstance(response, GetNodePropertyA)
        assert isinstance(response.result, Result)
        return pickle.loads(response.data)

    async def set_node_property(self, node: str, prop: str, value: Any) -> None:
        assert self._stub is not None
        path = NodePropertyPath(node=node, prop=prop)
        encoded_data = self._pickling(value)
        request = SetNodePropertyQ(path=path, data=encoded_data)
        response = await self._stub.SetNodeProperty(request, **self._options)
        assert isinstance(response, SetNodePropertyA)
        assert isinstance(response.result, Result)

    async def send_signal(
        self,
        name: Optional[str] = None,
        inject_slots: Optional[List[BoxData]] = None,
        extract_slots: Optional[List[BoxRequest]] = None,
    ) -> List[BoxData]:
        assert self._stub is not None
        request = SendSignalQ(
            name=name if name else str(),
            inject_slots=cvt_node_slot_datas(inject_slots, self._pickling),
            extract_slots=cvt_node_slot_data_requests(extract_slots),
        )
        response = await self._stub.SendSignal(request, **self._options)
        assert isinstance(response, SendSignalA)
        assert isinstance(response.result, Result)
        return cvt_box_datas(response.extracted_slots, self._unpickling)


def create_rpc_client(address: str, timeout: Optional[float] = None) -> RpcClient:
    return RpcClient(address, timeout)
