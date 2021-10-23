# -*- coding: utf-8 -*-

import asyncio
import pickle
import grpc
from typing import Any
from grpc.aio import ServicerContext, Server
from recc.argparse.config.daemon_config import DaemonConfig
from recc.plugin.plugin import (
    Plugin,
    NAME_ON_PACKET,
    NAME_ON_PICKLING,
)
from recc.log.logging import recc_daemon_logger as logger
from recc.proto.daemon.daemon_api_pb2 import PacketQ, PacketA
from recc.proto.daemon.daemon_api_pb2_grpc import (
    DaemonApiServicer,
    add_DaemonApiServicer_to_server,
)
from recc.init.default import (
    init_logger,
    init_json_driver,
    init_xml_driver,
    init_yaml_driver,
    init_loop_driver,
)
from recc.variables.rpc import (
    DEFAULT_GRPC_OPTIONS,
    DEFAULT_PICKLE_PROTOCOL_VERSION,
    DEFAULT_PICKLE_ENCODING,
)


class DaemonServicer(DaemonApiServicer):
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._pickling_protocol_version = DEFAULT_PICKLE_PROTOCOL_VERSION
        self._unpickling_encoding = DEFAULT_PICKLE_ENCODING

    def _pickling(self, data: Any) -> bytes:
        return pickle.dumps(data, protocol=self._pickling_protocol_version)

    def _unpickling(self, data: bytes) -> Any:
        return pickle.loads(data, encoding=self._unpickling_encoding)

    async def Packet(self, request: PacketQ, context: ServicerContext) -> PacketA:
        logger.info(f"Packet(method={request.method})")
        if not self._plugin.exists_packet_func:
            raise RuntimeError(f"Not exists `{NAME_ON_PACKET}` method")
        code, headers, content = await self._plugin.call_packet(
            request.method, request.headers, request.content
        )
        result_content = content if content else bytes()
        return PacketA(code=code, headers=headers, content=result_content)

    async def Pickling(self, request: PacketQ, context: ServicerContext) -> PacketA:
        logger.info(f"Pickling(method={request.method})")
        if not self._plugin.exists_pickling_func:
            raise RuntimeError(f"Not exists `{NAME_ON_PICKLING}` method")
        decoded_content = self._unpickling(request.content)
        code, headers, content = await self._plugin.call_pickling(
            request.method, request.headers, decoded_content
        )
        encoded_content = self._pickling(content)
        return PacketA(code=code, headers=headers, content=encoded_content)


def create_daemon_server(address: str, plugin: Plugin) -> Server:
    servicer = DaemonServicer(plugin)
    server = grpc.aio.server(options=DEFAULT_GRPC_OPTIONS)
    server.add_insecure_port(address)
    add_DaemonApiServicer_to_server(servicer, server)
    return server


async def run_daemon_server(config: DaemonConfig) -> None:
    plugin = Plugin(config.daemon_file)
    server = create_daemon_server(config.daemon_address, plugin)
    logger.info(f"Daemon server start: {config.daemon_file}")

    if plugin.exists_open:
        await plugin.call_open()

    await server.start()

    try:
        logger.info("SERVER IS RUNNING !!")

        await server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(0)
    finally:
        if plugin.exists_close:
            await plugin.call_close()
        logger.info(f"Daemon server done: {config.daemon_file}")


def run_daemon_until_complete(config: DaemonConfig) -> int:
    try:
        init_logger(config.log_config, config.log_level)
        init_json_driver(config.json_driver)
        init_xml_driver(config.xml_driver)
        init_yaml_driver(config.yaml_driver)
        init_loop_driver(config.loop_driver)

        asyncio.run(run_daemon_server(config))
        logger.info("Daemon completed successfully.")
        return 0
    except KeyboardInterrupt:
        logger.info("Received an interrupt.")
        return 0
    except BaseException as e:
        logger.exception(e)
        return 1
