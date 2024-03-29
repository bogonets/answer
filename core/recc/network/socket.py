# -*- coding: utf-8 -*-

from socket import (
    AF_INET,
    AF_INET6,
    SO_REUSEADDR,
    SO_REUSEPORT,
    SOCK_STREAM,
    SOL_SOCKET,
    socket,
)
from typing import Optional

from recc.logging.logging import recc_logger as logger
from recc.network.address_family import get_ip_address_family


def bind_socket(
    bind: str,
    port: int,
    reuse_address=False,
    reuse_port=False,
) -> Optional[socket]:

    family: int
    try:
        family = get_ip_address_family(bind)
    except ValueError:
        logger.error("The bind argument must be ipv4 or ipv6.")
        return None

    assert family == AF_INET or family == AF_INET6

    sock: Optional[socket] = None
    try:
        logger.info(f"Socket(bind={bind},port={port}) binding ...")
        sock = socket(family=family, type=SOCK_STREAM)

        # This is how to clear the `TIME_WAIT` time
        # when restarting the program to speed up debugging.
        if reuse_address:
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        if reuse_port:
            sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)

        sock.bind((bind, port))
        logger.info("Socket binding success.")
        return sock
    except OSError as e:
        logger.error(f"Socket binding failed: {e}")
        if sock is not None:
            sock.close()
        return None


def test_bind(bind: str, port: int) -> bool:
    sock: Optional[socket] = None
    try:
        sock = bind_socket(bind, port)
    except:  # noqa
        return False
    else:
        return True
    finally:
        if sock is not None:
            sock.close()
