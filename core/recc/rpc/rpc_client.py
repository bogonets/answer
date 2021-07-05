# -*- coding: utf-8 -*-

import asyncio
import grpc
import pickle
from typing import Optional, Callable, List, Any, TypeVar
from grpc.aio._channel import Channel  # noqa
from recc.exception.recc_error import RECC_CODE_TO_ERROR_TYPE_MAP, ReccRpcResponseError
from recc.mime.mime_codec_register import MimeCodecRegister, get_global_mime_register
from recc.serializable.json import serialize_json_text
from recc.blueprint.blueprint import BpTask
from recc.proto.api_pb2_grpc import ReccApiStub
from recc.variables.rpc import DEFAULT_GRPC_OPTIONS
from recc.vs.box import BoxData, BoxRequest
from recc.rpc.rpc_converter import (
    cvt_box_datas,
    cvt_node_slot_data_requests,
    cvt_node_slot_datas,
)
from recc.proto.api_pb2 import (
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

_T = TypeVar("_T")

DEFAULT_TIMEOUT = 32.0
DEFAULT_RESTART_DURATION = 5.0
DEFAULT_RESTART_COUNT = 5
DEFAULT_HEARTBEAT_TIMEOUT = 5.0


# def generate_test_q():
#     for i in range(10):
#         yield api.TestQ(msg=f"Q[{i}]")
#
#
# async def guide_list(stub: ReccApiStub) -> None:
#     async for response in stub.ServerStreamingTest(api.TestQ(msg="Q")):
#         print(f"SS -> TestA({response.msg})")
#
#
# async def guide_route_chat(stub: ReccApiStub) -> None:
#     async for response in stub.BidirectionalStreamingTest(generate_test_q()):
#         print(f"BS -> {response.msg}")
#
#
# async def test_node_client(address=DEFAULT_NODE_ADDRESS) -> None:
#     async with grpc.aio.insecure_channel(address) as channel:
#         stub = ReccApiStub(channel)
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
    timeout: Optional[float] = None,
) -> bool:
    async with grpc.aio.insecure_channel(
        address, options=DEFAULT_GRPC_OPTIONS
    ) as channel:
        # grpc.channel_ready_future(channel)
        stub = ReccApiStub(channel)
        options = dict()
        if timeout is not None:
            options["timeout"] = timeout
        response = await stub.Heartbeat(Pit(delay=delay), **options)
    return response.ok


async def try_connection(
    address: str,
    heartbeat_timeout: Optional[float] = None,
    delay: Optional[float] = None,
    max_attempts: Optional[int] = None,
    *,
    try_cb: Callable[[int, int], None] = None,
    retry_cb: Callable[[int, int], None] = None,
    success_cb: Callable[[int, int], None] = None,
    failure_cb: Callable[[int, int], None] = None,
) -> bool:
    retry_delay = delay if delay else DEFAULT_RESTART_DURATION
    retry_count = max_attempts if max_attempts else DEFAULT_RESTART_COUNT
    loop_timeout = heartbeat_timeout if heartbeat_timeout else DEFAULT_HEARTBEAT_TIMEOUT
    i = 0
    while i < retry_count:
        try:
            if try_cb:
                try_cb(i, retry_count)
            if await heartbeat(address, 0, loop_timeout):
                if success_cb:
                    success_cb(i, retry_count)
                return True
        except:  # noqa
            pass

        i += 1
        if i < retry_count:
            if retry_cb:
                retry_cb(i, retry_count)
            await asyncio.sleep(retry_delay)

    if failure_cb:
        failure_cb(i, retry_count)
    return False


def _check_result_code(code: int, msg: str) -> None:
    if code == 0:
        return
    if code in RECC_CODE_TO_ERROR_TYPE_MAP:
        raise RECC_CODE_TO_ERROR_TYPE_MAP[code](msg)
    else:
        raise ReccRpcResponseError(f"Result(code={code},msg='{msg}')")


def _check_result(result) -> None:
    assert isinstance(result, Result)
    _check_result_code(result.code, result.msg)


class RpcClient:

    _channel: Optional[Channel] = None
    _stub: Optional[ReccApiStub] = None

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
        self._stub = ReccApiStub(self._channel)
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
        _check_result(response.result)

    async def set_task_blueprint_json(self, task_json: str) -> None:
        assert self._stub is not None
        request = SetTaskBlueprintQ(json=task_json)
        response = await self._stub.SetTaskBlueprint(request, **self._options)
        assert isinstance(response, SetTaskBlueprintA)
        _check_result(response.result)

    async def set_task_blueprint(self, task: BpTask, version=1) -> None:
        task_json = serialize_json_text(version, task)
        await self.set_task_blueprint_json(task_json)

    async def get_node_property(self, node: str, prop: str) -> Any:
        assert self._stub is not None
        path = NodePropertyPath(node=node, prop=prop)
        request = GetNodePropertyQ(path=path)
        response = await self._stub.GetNodeProperty(request, **self._options)
        assert isinstance(response, GetNodePropertyA)
        _check_result(response.result)
        return pickle.loads(response.data)

    async def set_node_property(self, node: str, prop: str, value: Any) -> None:
        assert self._stub is not None
        path = NodePropertyPath(node=node, prop=prop)
        encoded_data = self._pickling(value)
        request = SetNodePropertyQ(path=path, data=encoded_data)
        response = await self._stub.SetNodeProperty(request, **self._options)
        assert isinstance(response, SetNodePropertyA)
        _check_result(response.result)

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
        _check_result(response.result)
        return cvt_box_datas(response.extracted_slots, self._unpickling)


def create_rpc_client(address: str, timeout: Optional[float] = None) -> RpcClient:
    return RpcClient(address, timeout)
