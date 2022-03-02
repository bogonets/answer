# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Tuple
from enum import Enum
from recc.uri.host_port import parse_host_port


class RpcSchemeType(Enum):
    Dns = 0
    Unix = 1
    UnixAbstract = 2
    Ipv4 = 3
    Ipv6 = 4


NOT_FOUND_INDEX = -1

SCHEME_DNS = "dns:"
SCHEME_UNIX = "unix:"
SCHEME_UNIX_ABSTRACT = "unix-abstract:"
SCHEME_IPV4 = "ipv4:"
SCHEME_IPV6 = "ipv6:"

SCHEME_DNS_LEN = len(SCHEME_DNS)
SCHEME_UNIX_LEN = len(SCHEME_UNIX)
SCHEME_UNIX_ABSTRACT_LEN = len(SCHEME_UNIX_ABSTRACT)
SCHEME_IPV4_LEN = len(SCHEME_IPV4)
SCHEME_IPV6_LEN = len(SCHEME_IPV6)


def get_rpc_scheme_type(address: str) -> RpcSchemeType:
    if address.startswith(SCHEME_DNS):
        return RpcSchemeType.Dns
    elif address.startswith(SCHEME_UNIX):
        return RpcSchemeType.Unix
    elif address.startswith(SCHEME_UNIX_ABSTRACT):
        return RpcSchemeType.UnixAbstract
    elif address.startswith(SCHEME_IPV4):
        return RpcSchemeType.Ipv4
    elif address.startswith(SCHEME_IPV6):
        return RpcSchemeType.Ipv6

    # https://github.com/grpc/grpc/blob/master/doc/naming.md
    # If no scheme prefix is specified or the scheme is unknown,
    # the dns scheme is used by default.
    return RpcSchemeType.Dns


OPENING_AUTHORITY = "//"
OPENING_AUTHORITY_LEN = len(OPENING_AUTHORITY)

CLOSING_AUTHORITY = "/"
CLOSING_AUTHORITY_LEN = len(CLOSING_AUTHORITY)


class RpcDnsAddress(NamedTuple):
    """
    Syntax: ``dns:[//authority/]host[:port]``
    """

    authority: Optional[str]
    host: str
    port: Optional[int]

    @property
    def authority_tuple(self) -> Optional[Tuple[str, Optional[int]]]:
        if not self.authority:
            return None

        host_port = parse_host_port(self.authority)
        return host_port.host, host_port.port

    @property
    def authority_host(self) -> Optional[str]:
        host_port = self.authority_tuple
        return host_port[0] if host_port is not None else None

    @property
    def authority_port(self) -> Optional[int]:
        host_port = self.authority_tuple
        return host_port[1] if host_port is not None else None


def parse_rpc_dns_address(address: str) -> RpcDnsAddress:
    if get_rpc_scheme_type(address) != RpcSchemeType.Dns:
        raise ValueError(f"Invalid DNS scheme: {address}")

    authority: Optional[str]

    if address.startswith(SCHEME_DNS):
        body = address[SCHEME_DNS_LEN:]
    else:
        body = address

    if body.startswith(OPENING_AUTHORITY):
        closing_authority_index = body[OPENING_AUTHORITY_LEN:].find(CLOSING_AUTHORITY)
        if closing_authority_index == NOT_FOUND_INDEX:
            raise ValueError(
                f"Could not find the closing character ('{CLOSING_AUTHORITY}')"
                f"in the authority section: '{address}'"
            )

        authority_last_index = OPENING_AUTHORITY_LEN + closing_authority_index
        authority = body[OPENING_AUTHORITY_LEN:authority_last_index]
        host_port_begin = authority_last_index + CLOSING_AUTHORITY_LEN
        host_port_body = body[host_port_begin:]
    else:
        authority = None
        host_port_body = body

    host_port = parse_host_port(host_port_body)
    return RpcDnsAddress(authority, host_port.host, host_port.port)
