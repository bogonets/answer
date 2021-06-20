# -*- coding: utf-8 -*-

import asyncio
import grpc
from recc.argparse.config.task_config import TaskConfig
from recc.init.default import init_logger, init_json_driver, init_loop_driver
from recc.log.logging import recc_rpc_logger as logger
from recc.proto.api_pb2_grpc import add_ReccApiServicer_to_server
from recc.rpc.async_rpc_client import try_connection
from recc.rpc.async_rpc_server import TaskRpcServicer
from recc.variables.rpc_options import DEFAULT_GRPC_OPTIONS


class _ServerInfo(object):

    __slots__ = ("servicer", "server", "port")

    def __init__(self, servicer: TaskRpcServicer, server: grpc.aio.Server, port: int):
        self.servicer = servicer
        self.server = server
        self.port = port


def create_task_server(config: TaskConfig) -> _ServerInfo:
    server = grpc.aio.server(options=DEFAULT_GRPC_OPTIONS)
    address = f"{config.task_bind}:{config.task_port}"
    really_port = server.add_insecure_port(address)
    servicer = TaskRpcServicer(config, really_port)
    add_ReccApiServicer_to_server(servicer, server)
    return _ServerInfo(servicer, server, really_port)


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

    await try_connection(
        address,
        try_cb=_try_cb,
        retry_cb=_retry_cb,
        success_cb=_success_cb,
        failure_cb=_failure_cb,
    )


async def run_task_server(config: TaskConfig, wait_connect=True) -> None:
    logger.info("Start the task server")
    logger.info(f"- bind: '{config.task_bind}'")
    logger.info(f"- port: {config.task_port}")
    logger.info(f"- register: '{config.task_register}'")
    logger.info(f"- workspace: '{config.task_workspace}'")

    server_info = create_task_server(config)
    # servicer = server_info.servicer
    server = server_info.server
    really_port = server_info.port
    await server.start()

    if wait_connect:
        await wait_connectable(f"localhost:{really_port}")

    try:
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
