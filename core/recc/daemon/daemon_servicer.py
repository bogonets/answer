# -*- coding: utf-8 -*-

import pickle
import grpc
from asyncio import sleep
from asyncio import run as asyncio_run
from typing import Optional, Any
from grpc.aio import ServicerContext
from recc.aio.connection import try_connection
from recc.argparse.config.daemon_config import DaemonConfig
from recc.plugin.plugin import (
    Plugin,
    NAME_ON_PACKET,
    NAME_ON_PICKLING,
)
from recc.log.logging import recc_daemon_logger as logger
from recc.network.uds import is_uds_family
from recc.proto.daemon.daemon_api_pb2 import Pit, Pat, PacketQ, PacketA
from recc.proto.daemon.daemon_api_pb2_grpc import (
    DaemonApiServicer,
    add_DaemonApiServicer_to_server,
)
from recc.daemon.daemon_client import heartbeat
from recc.init.default import (
    init_logger,
    init_json_driver,
    init_xml_driver,
    init_yaml_driver,
    init_loop_driver,
)
from recc.variables.rpc import (
    ACCEPTED_UDS_PORT_NUMBER,
    DEFAULT_GRPC_OPTIONS,
    DEFAULT_PICKLE_PROTOCOL_VERSION,
    DEFAULT_PICKLE_ENCODING,
)


class DaemonServicer(DaemonApiServicer):
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._pickling_protocol_version = DEFAULT_PICKLE_PROTOCOL_VERSION
        self._unpickling_encoding = DEFAULT_PICKLE_ENCODING

    @property
    def plugin(self) -> Plugin:
        return self._plugin

    def _pickling(self, data: Any) -> bytes:
        return pickle.dumps(data, protocol=self._pickling_protocol_version)

    def _unpickling(self, data: bytes) -> Any:
        return pickle.loads(data, encoding=self._unpickling_encoding)

    async def Heartbeat(self, request: Pit, context: ServicerContext) -> Pat:
        logger.info(f"Heartbeat(delay={request.delay})")
        await sleep(delay=request.delay)
        return Pat(ok=True)

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


class _AcceptInfo(object):

    __slots__ = ("servicer", "server", "accepted_port_number")

    def __init__(
        self,
        servicer: DaemonServicer,
        server: grpc.aio.Server,
        accepted_port_number: Optional[int] = None,
    ):
        self.servicer = servicer
        self.server = server
        self.accepted_port_number = accepted_port_number


def create_daemon_server(address: str, daemon_file: str) -> _AcceptInfo:
    servicer = DaemonServicer(Plugin(daemon_file))
    logger.info(f"Daemon servicer address: {address}")

    server = grpc.aio.server(options=DEFAULT_GRPC_OPTIONS)
    accepted_port_number = server.add_insecure_port(address)

    add_DaemonApiServicer_to_server(servicer, server)

    if is_uds_family(address):
        assert accepted_port_number == ACCEPTED_UDS_PORT_NUMBER
        logger.info("Daemon socket type: Unix Domain Socket")
        return _AcceptInfo(servicer, server)
    else:
        assert accepted_port_number != ACCEPTED_UDS_PORT_NUMBER
        logger.info("Daemon socket type: IP Address")
        logger.info(f"Accepted port number: {accepted_port_number}")
        return _AcceptInfo(servicer, server, accepted_port_number)


async def wait_connectable(address: str) -> bool:
    def _try_cb(i: int, max_attempts: int) -> None:
        assert 0 <= i <= max_attempts
        attempts_msg = f"{i+1}/{max_attempts}"
        logger.debug(f"wait_connectable() -> Try connection ({attempts_msg}) ...")

    def _retry_cb(i: int, max_attempts: int) -> None:
        assert 0 <= i <= max_attempts
        attempts_msg = f"{i+1}/{max_attempts}"
        logger.debug(f"wait_connectable() -> Retry connection ({attempts_msg}) ...")

    def _success_cb(i: int, max_attempts: int) -> None:
        assert 0 <= i <= max_attempts
        logger.info("wait_connectable() -> Self connection successful !!")

    def _failure_cb(i: int, max_attempts: int) -> None:
        assert 0 <= i <= max_attempts
        logger.debug("wait_connectable() -> Self connection failure.")

    logger.info(f"Try connection address: {address}")
    return await try_connection(
        lambda: heartbeat(address),
        try_cb=_try_cb,
        retry_cb=_retry_cb,
        success_cb=_success_cb,
        failure_cb=_failure_cb,
    )


async def run_daemon_server(config: DaemonConfig, wait_connect=True) -> None:
    logger.info(f"Start the daemon server: {config.daemon_file}")

    accept_info = create_daemon_server(config.daemon_address, config.daemon_file)
    plugin = accept_info.servicer.plugin
    server = accept_info.server
    accepted_port_number = accept_info.accepted_port_number

    if plugin.exists_open:
        await plugin.call_open()

    await server.start()

    if wait_connect:
        if accepted_port_number is None:
            await wait_connectable(config.daemon_address)
        else:
            await wait_connectable(f"localhost:{accepted_port_number}")

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

        asyncio_run(run_daemon_server(config))
        logger.info("Daemon completed successfully.")
        return 0
    except KeyboardInterrupt:
        logger.info("Received an interrupt.")
        return 0
    except BaseException as e:
        logger.exception(e)
        return 1
