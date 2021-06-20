# -*- coding: utf-8 -*-

import os
import asyncio
import pickle
from grpc.aio import ServicerContext
from typing import Any
from recc.exception.recc_error import ReccError
from recc.argparse.config.task_config import TaskConfig

# from recc.serializable.json import deserialize_json_text
# from recc.blueprint.blueprint import BpTask

from recc.log.logging import recc_rpc_logger as logger
from recc.storage.async_workspace import AsyncWorkspace
from recc.rpc.rpc_converter import (
    cvt_node_slot_data,
    cvt_box_data,
    cvt_box_request,
)

from recc.vs.task import Task
from recc.proto.api_pb2_grpc import (
    ReccApiServicer,
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


class TaskRpcServicer(ReccApiServicer):
    """
    RECC Task RPC Servicer.
    """

    def __init__(
        self,
        config: TaskConfig,
        really_port: int,
    ):
        self._config = config
        self._bind = config.task_bind
        self._port = really_port
        self._register = config.task_register
        self._workspace = AsyncWorkspace(config.task_workspace)
        self._pickling_protocol_version = 5
        self._unpickling_encoding = "latin1"
        self._task = Task()
        self._setup()

    def _setup(self) -> None:
        os.chdir(self._workspace.working_dir)

    def _pickling(self, data: Any) -> bytes:
        return pickle.dumps(data, protocol=self._pickling_protocol_version)

    def _unpickling(self, data: bytes) -> Any:
        return pickle.loads(data, encoding=self._unpickling_encoding)

    @property
    def workspace(self) -> AsyncWorkspace:
        return self._workspace

    async def Heartbeat(self, request: Pit, context: ServicerContext) -> Pat:
        logger.info(f"Heartbeat(delay={request.delay})")
        await asyncio.sleep(delay=request.delay)
        return Pat(ok=True)

    async def Echo(self, request: Ping, context: ServicerContext) -> Pong:
        logger.info(f"Echo(msg={request.msg})")
        return Pong(msg=request.msg)

    async def EchoData(self, request: Data, context: ServicerContext) -> Data:
        logger.info(f"EchoData(data={len(request.data)}byte)")
        return Data(data=request.data)

    async def GetWorkspaceSubdir(
        self, request: Empty, context: ServicerContext
    ) -> Names:
        logger.info("GetWorkspaceDirs()")
        subdir = self._workspace.get_workspace_subdir()
        return Names(names=subdir)

    async def GetTemplateNames(self, request: Empty, context: ServicerContext) -> Names:
        logger.info("GetTemplateNames()")
        names = [key.name for key in self._workspace.get_template_keys()]
        return Names(names=names)

    async def UploadTemplate(
        self, request: UploadTemplateQ, context: ServicerContext
    ) -> UploadTemplateA:
        assert isinstance(request.tar, TarFile)
        logger.info(f"UploadTemplate(data={len(request.tar.data)}byte)")
        try:
            self._workspace.decompress_templates(request.tar.data)
            self._workspace.refresh_templates()
        except ReccError as e:
            return UploadTemplateA(result=Result(code=e.code, msg=str(e)))
        else:
            return UploadTemplateA(result=Result(code=0))

    async def SetTaskBlueprint(
        self, request: SetTaskBlueprintQ, context: ServicerContext
    ) -> SetTaskBlueprintA:
        json_text = request.json
        logger.info(f"SetTaskBlueprint(json={json_text})")
        template_manager = self._workspace.get_template_manager()
        self._task.clear()
        self._task.set_blueprint_json(json_text, 1, template_manager)
        return SetTaskBlueprintA(result=Result(code=0))

    async def GetNodeProperty(
        self, request: GetNodePropertyQ, context: ServicerContext
    ) -> GetNodePropertyA:
        assert isinstance(request.path, NodePropertyPath)
        node = request.path.node
        prop = request.path.prop
        logger.info(f"GetNodeProperty(node={node},prop={prop})")
        response_data = self._task.node_get(node, prop)
        data = self._pickling(response_data)
        return GetNodePropertyA(result=Result(code=0), data=data)

    async def SetNodeProperty(
        self, request: SetNodePropertyQ, context: ServicerContext
    ) -> SetNodePropertyA:
        assert isinstance(request.path, NodePropertyPath)
        node = request.path.node
        prop = request.path.prop
        data = pickle.loads(request.data)
        logger.info(f"SetNodeProperty(node={node},prop={prop},data={len(data)}byte)")
        self._task.node_set(node, prop, data)
        return SetNodePropertyA(result=Result(code=0))

    async def SendSignal(
        self, request: SendSignalQ, context: ServicerContext
    ) -> SendSignalA:
        name = request.name
        inject_slots = [cvt_box_data(s, self._unpickling) for s in request.inject_slots]
        extract_slots = [cvt_box_request(s) for s in request.extract_slots]
        params_msg = f"inject={len(inject_slots)},extract={len(extract_slots)}"
        logger.info(f"SendSignal(name={name},{params_msg})")
        result = self._task.send_signal(name, inject_slots, extract_slots)
        extracted_slots = [cvt_node_slot_data(s, self._pickling) for s in result]
        return SendSignalA(result=Result(code=0), extracted_slots=extracted_slots)

    # async def Test(
    #     self,
    #     request: api.TestQ,
    #     context: grpc.aio.ServicerContext,
    # ) -> api.TestA:
    #     # logger.info(f"RPC/Test(msg={request.msg})")
    #     print(f"RPC/Test(msg={request.msg})")
    #     return api.TestA(msg=request.msg)
    #
    # async def ClientStreamingTest(
    #     self,
    #     request_iterator: AsyncIterable[api.TestQ],
    #     context: grpc.aio.ServicerContext,
    # ) -> api.TestA:
    #     total = ""
    #     async for request in request_iterator:
    #         print(f"RPC/ClientStreamingTest(msg={request.msg}) ...")
    #         total += request.msg
    #     print(f"RPC/ClientStreamingTest() Done -> {total}")
    #     return api.TestA(msg=total)
    #
    # async def ServerStreamingTest(
    #     self,
    #     request: api.TestQ,
    #     context: grpc.aio.ServicerContext,
    # ) -> AsyncIterable[api.TestA]:
    #     print(f"RPC/ServerStreamingTest(msg={request.msg})")
    #     for i in range(10):
    #         generated_msg = f"{request.msg}[{i}]"
    #         print(f"RPC/ServerStreamingTest() Streaming -> {generated_msg}")
    #         yield api.TestA(msg=f"{generated_msg}")
    #     print("RPC/ServerStreamingTest() Done")
    #
    # async def BidirectionalStreamingTest(
    #     self,
    #     request_iterator: AsyncIterable[api.TestQ],
    #     context: grpc.aio.ServicerContext,
    # ) -> AsyncIterable[api.TestA]:
    #     total = ""
    #     async for request in request_iterator:
    #         print(f"RPC/BidirectionalStreamingTest() Streaming -> {request.msg}")
    #         total += request.msg
    #         yield api.TestA(msg=f"{request.msg}")
    #     print(f"RPC/BidirectionalStreamingTest() Last streaming -> {total}")
    #     yield api.TestA(msg=total)
    #     print("RPC/BidirectionalStreamingTest() Done")
