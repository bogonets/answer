# -*- coding: utf-8 -*-

import pickle
import grpc
from asyncio import sleep
from asyncio import run as asyncio_run
from typing import Optional, Any
from grpc.aio import ServicerContext
from recc.aio.connection import try_connection
from recc.argparse.config.daemon_config import DaemonConfig
from recc.plugin.plugin import Plugin, NAME_ON_PACKET, NAME_ON_PICKLING
from recc.log.logging import recc_daemon_logger as logger
from recc.network.uds import is_uds_family
from recc.proto.daemon.daemon_api_pb2 import Pit, Pat, InitQ, InitA, PacketQ, PacketA
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

INIT_CODE_SUCCESS = 0
INIT_CODE_NOT_FOUND_INIT_FUNCTION = 1


class DaemonServicer(DaemonApiServicer):
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._pickling_protocol_version = DEFAULT_PICKLE_PROTOCOL_VERSION
        self._unpickling_encoding = DEFAULT_PICKLE_ENCODING

        self.database_type: Optional[str] = None
        self.database_host: Optional[str] = None
        self.database_port: Optional[int] = None
        self.database_user: Optional[str] = None
        self.database_pw: Optional[str] = None
        self.database_name: Optional[str] = None
        self.database_timeout: Optional[float] = None

        self.storage_type: Optional[str] = None
        self.storage_host: Optional[str] = None
        self.storage_port: Optional[int] = None
        self.storage_user: Optional[str] = None
        self.storage_pw: Optional[str] = None
        self.storage_region: Optional[str] = None
        self.storage_timeout: Optional[float] = None

    @property
    def plugin(self) -> Plugin:
        return self._plugin

    def _pickling(self, data: Any) -> bytes:
        return pickle.dumps(data, protocol=self._pickling_protocol_version)

    def _unpickling(self, data: bytes) -> Any:
        return pickle.loads(data, encoding=self._unpickling_encoding)

    async def on_open(self) -> None:
        logger.info("Daemon opening ...")
        if self._plugin.exists_open:
            await self._plugin.call_open()
        logger.info("Daemon opened.")

    async def on_close(self) -> None:
        logger.info("Daemon closing ...")
        if self._plugin.exists_close:
            await self._plugin.call_close()
        logger.info("Daemon closed.")

    async def Heartbeat(self, request: Pit, context: ServicerContext) -> Pat:
        logger.debug(f"Heartbeat(delay={request.delay})")
        await sleep(delay=request.delay)
        return Pat(ok=True)

    async def Init(self, request: InitQ, context: ServicerContext) -> InitA:
        logger.debug(f"Init(args={request.args},kwargs={request.kwargs})")
        if not self._plugin.exists_init_func:
            return InitA(code=INIT_CODE_NOT_FOUND_INIT_FUNCTION)
        args = [str(a) for a in request.args]
        kwargs = {str(k): str(v) for k, v in request.kwargs.items()}
        await self._plugin.call_init(*args, **kwargs)
        return InitA(code=INIT_CODE_SUCCESS)

    async def Packet(self, request: PacketQ, context: ServicerContext) -> PacketA:
        logger.debug(f"Packet(method={request.method})")
        if not self._plugin.exists_packet_func:
            raise RuntimeError(f"Not exists `{NAME_ON_PACKET}` method")
        code, headers, content = await self._plugin.call_packet(
            request.method, request.headers, request.content
        )
        result_content = content if content else bytes()
        return PacketA(code=code, headers=headers, content=result_content)

    async def Pickling(self, request: PacketQ, context: ServicerContext) -> PacketA:
        logger.debug(f"Pickling(method={request.method})")
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


def create_daemon_server(
    address: str,
    daemon_file: str,
    daemon_packages_dir: Optional[str] = None,
) -> _AcceptInfo:
    servicer = DaemonServicer(Plugin(daemon_file, daemon_packages_dir))
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

    accept_info = create_daemon_server(
        config.daemon_address,
        config.daemon_file,
        config.daemon_packages_dir,
    )
    servicer = accept_info.servicer
    await servicer.on_open()
    server = accept_info.server
    accepted_port_number = accept_info.accepted_port_number

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
        await servicer.on_close()
        logger.info(f"Daemon server done: {config.daemon_file}")


def run_daemon_until_complete(config: DaemonConfig) -> int:
    try:
        init_logger(config.log_config, config.log_level, config.log_simply)
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
