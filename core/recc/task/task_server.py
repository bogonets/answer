# -*- coding: utf-8 -*-

import grpc

from typing import Optional
from asyncio import run as asyncio_run
from recc.aio.connection import try_connection
from recc.argparse.config.task_config import TaskConfig
from recc.init.default import (
    init_logger,
    init_json_driver,
    init_xml_driver,
    init_yaml_driver,
    init_loop_driver,
)
from recc.logging.logging import recc_rpc_logger as logger
from recc.proto.rpc.rpc_api_pb2_grpc import add_RpcApiServicer_to_server
from recc.network.uds import is_uds_family
from recc.rpc.rpc_client import heartbeat
from recc.rpc.rpc_servicer import RpcServicer
from recc.variables.rpc import DEFAULT_GRPC_OPTIONS, ACCEPTED_UDS_PORT_NUMBER


class _AcceptInfo(object):

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


def create_task_server(config: TaskConfig) -> _AcceptInfo:
    servicer = RpcServicer(config)
    rpc_address = servicer.get_rpc_address()

    logger.info(f"RPC servicer address: {rpc_address}")

    server = grpc.aio.server(options=DEFAULT_GRPC_OPTIONS)
    accepted_port_number = server.add_insecure_port(rpc_address)

    add_RpcApiServicer_to_server(servicer, server)

    if is_uds_family(rpc_address):
        assert accepted_port_number == ACCEPTED_UDS_PORT_NUMBER
        logger.info("RPC socket type: Unix Domain Socket")
        return _AcceptInfo(servicer, server)
    else:
        assert accepted_port_number != ACCEPTED_UDS_PORT_NUMBER
        logger.info("RPC socket type: IP Address")
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


async def run_task_server(config: TaskConfig, wait_connect=True) -> None:
    logger.info("Start the task server")

    accept_info = create_task_server(config)
    servicer = accept_info.servicer
    server = accept_info.server
    accepted_port_number = accept_info.accepted_port_number
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
        init_logger(config.log_config, config.log_level, config.log_simply)
        init_json_driver(config.json_driver)
        init_xml_driver(config.xml_driver)
        init_yaml_driver(config.yaml_driver)
        init_loop_driver(config.loop_driver)

        asyncio_run(run_task_server(config))
        logger.info("Task server completed successfully.")
        return 0
    except KeyboardInterrupt:
        logger.info("Received an interrupt.")
        return 0
    except BaseException as e:
        logger.exception(e)
        return 1
