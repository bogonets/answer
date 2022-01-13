# -*- coding: utf-8 -*-

import pickle
import grpc
from asyncio import sleep
from asyncio import run as asyncio_run
from typing import Optional, Any, List
from inspect import signature, iscoroutinefunction
from multiprocessing.shared_memory import SharedMemory
from grpc.aio import ServicerContext
from recc.aio.connection import try_connection
from recc.argparse.config.daemon_config import DaemonConfig
from recc.plugin.plugin import Plugin
from recc.log.logging import recc_daemon_logger as logger
from recc.network.uds import is_uds_family
from recc.inspect.type_origin import get_type_origin
from recc.conversion.boolean import str_to_bool
from recc.serialization.serialize import serialize_default
from recc.serialization.deserialize import deserialize_default
from recc.serialization.byte import (
    COMPRESS_LEVEL_BEST,
    orjson_zlib_encoder,
    orjson_zlib_decoder,
)
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


def _test_shared_memory(name: str, password: str) -> bool:
    if name and password:
        try:
            sm = SharedMemory(name=name)
            return bytes(sm.buf[:]) == bytes.fromhex(password)
        except:  # noqa
            pass
    return False


def _is_path_class(obj) -> bool:
    if not isinstance(obj, type):
        return False
    if issubclass(obj, str):
        return True
    if issubclass(obj, int):
        return True
    if issubclass(obj, float):
        return True
    if issubclass(obj, bool):
        return True
    return False


def _cast_builtin_type_from_string(data: str, cls) -> Any:
    assert isinstance(cls, type)
    if issubclass(cls, str):
        return data
    elif issubclass(cls, int):
        return int(data)
    elif issubclass(cls, float):
        return float(data)
    elif issubclass(cls, bool):
        return str_to_bool(data)
    return cls(data)  # type: ignore[call-arg]


class DaemonServicer(DaemonApiServicer):
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._pickling_protocol_version = DEFAULT_PICKLE_PROTOCOL_VERSION
        self._unpickling_encoding = DEFAULT_PICKLE_ENCODING
        self._zlib_compress_level = COMPRESS_LEVEL_BEST

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
        if self._plugin.exists_routes:
            self._plugin.update_routes()
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
        is_sm = _test_shared_memory(request.test_sm_name, request.test_sm_pass)
        return InitA(code=INIT_CODE_SUCCESS, is_sm=is_sm)

    async def _call_route(self, method: str, path: str, content: bytes) -> bytes:
        route, match_info = self._plugin.get_route(method, path)

        sig = signature(route)
        args: List[Any] = list()

        for key, param in sig.parameters.items():
            type_origin = get_type_origin(param)

            assert type_origin is not None
            assert isinstance(type_origin, type)

            # Path
            if _is_path_class(type_origin) and key in match_info:
                path_value = match_info[key]
                try:
                    path_arg = _cast_builtin_type_from_string(path_value, type_origin)
                    args.append(path_arg)
                except ValueError:
                    logger.debug(f"Type casting error for path parameter: {key}")
                    args.append(path_value)
            else:
                decoded_data = orjson_zlib_decoder(content)
                deserialize_object = deserialize_default(decoded_data, type_origin)
                args.append(deserialize_object)

        if iscoroutinefunction(route):
            result = await route(*args)
        else:
            result = route(*args)

        if result is None:
            return bytes()
        else:
            return orjson_zlib_encoder(
                serialize_default(result),
                self._zlib_compress_level,
            )

    async def Packet(self, request: PacketQ, context: ServicerContext) -> PacketA:
        method = request.method
        path = request.path
        sm_name = request.sm_name
        content_size = request.content_size
        logger.debug(f"Packet(method={method},path={path},content_size={content_size})")

        sm: Optional[SharedMemory]
        if sm_name and content_size > 0:
            sm = SharedMemory(name=sm_name)
            request_content = bytes(sm.buf[:content_size])
        else:
            sm = None
            request_content = request.content

        result = await self._call_route(method, path, request_content)
        result_size = len(result)

        if sm is not None and result and sm.size >= result_size:
            assert sm_name
            assert result_size >= 1
            sm.buf[:result_size] = result
            response_content = bytes()
        else:
            response_content = result

        return PacketA(content_size=result_size, content=response_content)


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
