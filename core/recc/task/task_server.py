# -*- coding: utf-8 -*-

import asyncio
import grpc
from typing import Optional
from ipaddress import ip_address
from recc.argparse.config.task_config import TaskConfig, get_task_config_members
from recc.init.default import init_logger, init_json_driver, init_loop_driver
from recc.log.logging import recc_rpc_logger as logger
from recc.proto.api_pb2_grpc import add_ReccApiServicer_to_server
from recc.rpc.rpc_client import try_connection
from recc.rpc.rpc_servicer import RpcServicer
from recc.variables.rpc import (
    DEFAULT_GRPC_OPTIONS,
    ACCEPTED_UDS_PORT_NUMBER,
    UNIX_URI_PREFIX,
    UNIX_ABSTRACT_URI_PREFIX,
)


class _ServerInfo(object):

    __slots__ = ("servicer", "server", "accepted_port_number")

    def __init__(
        self,
        servicer: RpcServicer,
        server: grpc.aio.Server,
        accepted_port_number: Optional[int] = None,
    ):
        self.servicer = servicer
        self.server = server
        self.accepted_port_number = accepted_port_number


def _is_uds_family(address: str) -> bool:
    if address.startswith(UNIX_URI_PREFIX):
        return True
    if address.startswith(UNIX_ABSTRACT_URI_PREFIX):
        return True
    return False


def _is_ip_address(address: str) -> int:
    try:
        ip_address(address)
    except ValueError:
        return False
    else:
        return True


def create_task_server(config: TaskConfig) -> _ServerInfo:
    servicer = RpcServicer(config)
    rpc_address = servicer.get_rpc_address()

    logger.info(f"RPC servicer address: {rpc_address}")

    server = grpc.aio.server(options=DEFAULT_GRPC_OPTIONS)
    accepted_port_number = server.add_insecure_port(rpc_address)

    add_ReccApiServicer_to_server(servicer, server)

    if _is_uds_family(rpc_address):
        assert accepted_port_number == ACCEPTED_UDS_PORT_NUMBER
        logger.info("RPC socket type: Unix Domain Socket")
        return _ServerInfo(servicer, server)
    else:
        assert accepted_port_number != ACCEPTED_UDS_PORT_NUMBER
        logger.info("RPC socket type: IP Address")
        logger.info(f"Accepted port number: {accepted_port_number}")
        return _ServerInfo(servicer, server, accepted_port_number)


async def wait_connectable(address: str) -> None:
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
    await try_connection(
        address,
        try_cb=_try_cb,
        retry_cb=_retry_cb,
        success_cb=_success_cb,
        failure_cb=_failure_cb,
    )


def _logging_config_value(config: TaskConfig, key: str) -> None:
    if not hasattr(config, key):
        return

    val = getattr(config, key)
    if isinstance(val, str):
        val_text = f"'{val}'"
    else:
        val_text = str(val)
    logger.info(f"- {key}: {val_text}")


def _logging_config(config: TaskConfig) -> None:
    global_keys = (
        "user",
        "group",
        "loop_driver",
        "json_driver",
        "suppress_print",
        "verbose",
        "teardown",
        "developer",
    )
    for global_key in global_keys:
        _logging_config_value(config, global_key)
    for key in get_task_config_members(ignore_global_members=True):
        _logging_config_value(config, key)


async def run_task_server(config: TaskConfig, wait_connect=True) -> None:
    logger.info("Start the task server")
    _logging_config(config)

    server_info = create_task_server(config)
    servicer = server_info.servicer
    server = server_info.server
    accepted_port_number = server_info.accepted_port_number
    await server.start()

    if wait_connect:
        address = servicer.get_rpc_address()
        if accepted_port_number is None:
            await wait_connectable(address)
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


def run_task_until_complete(config: TaskConfig) -> int:
    try:
        init_logger(config.log_config, config.log_level)
        init_json_driver(config.json_driver)
        init_loop_driver(config.loop_driver)

        asyncio.run(run_task_server(config))
        logger.info("Task server completed successfully.")
        return 0
    except KeyboardInterrupt:
        logger.info("Received an interrupt.")
        return 0
    except BaseException as e:
        logger.exception(e)
        return 1
