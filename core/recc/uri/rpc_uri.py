# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Tuple, List, Union
from socket import AF_INET, AF_INET6
from enum import Enum
from recc.uri.host_port import (
    parse_ipv4_or_domain_port,
    parse_ipv6_port,
    parse_host_port,
    OPENING_IPV6,
    CLOSING_IPV6,
)
from recc.network.address_family import get_ip_address_family


class RpcSchemeType(Enum):
    Dns = 0
    Unix = 1
    UnixAbstract = 2
    Ipv4 = 3
    Ipv6 = 4


NOT_FOUND_INDEX = -1

SCHEME_DNS = "dns:"
SCHEME_UNIX = "unix:"
SCHEME_UNIX2 = SCHEME_UNIX + "//"
SCHEME_UNIX_ABSTRACT = "unix-abstract:"
SCHEME_IPV4 = "ipv4:"
SCHEME_IPV6 = "ipv6:"

SCHEME_DNS_LEN = len(SCHEME_DNS)
SCHEME_UNIX_LEN = len(SCHEME_UNIX)
SCHEME_UNIX2_LEN = len(SCHEME_UNIX2)
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


def _parse_rpc_dns_address(address: str) -> RpcDnsAddress:
    assert get_rpc_scheme_type(address) == RpcSchemeType.Dns

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


def parse_rpc_dns_address(address: str) -> RpcDnsAddress:
    if get_rpc_scheme_type(address) != RpcSchemeType.Dns:
        raise ValueError(f"Invalid DNS scheme: {address}")
    return _parse_rpc_dns_address(address)


class RpcUnixAddress(NamedTuple):
    """
    Syntax: ``unix:path`` or ``unix://absolute_path``
    """

    path: str


def _parse_rpc_unix_address(address: str) -> RpcUnixAddress:
    assert get_rpc_scheme_type(address) == RpcSchemeType.Unix

    # [IMPORTANT]
    # Do not change the order of if-else statements.
    if address.startswith(SCHEME_UNIX2):
        absolute_path = address[SCHEME_UNIX2_LEN:]
        if absolute_path[0] != "/":
            raise ValueError(
                f"If you use the `{SCHEME_UNIX2}` prefix,"
                f"the path must be absolute: {address}"
            )
        return RpcUnixAddress(absolute_path)
    elif address.startswith(SCHEME_UNIX):
        return RpcUnixAddress(address[SCHEME_UNIX_LEN:])
    else:
        assert False, "Inaccessible section"


def parse_rpc_unix_address(address: str) -> RpcUnixAddress:
    if get_rpc_scheme_type(address) != RpcSchemeType.Unix:
        raise ValueError(f"Invalid Unix scheme: {address}")
    return _parse_rpc_unix_address(address)


class RpcUnixAbstractAddress(NamedTuple):
    """
    Syntax: ``unix-abstract:abstract_path``
    """

    abstract_path: str


def _parse_rpc_unix_abstract_address(address: str) -> RpcUnixAbstractAddress:
    assert get_rpc_scheme_type(address) == RpcSchemeType.UnixAbstract
    return RpcUnixAbstractAddress(address[SCHEME_UNIX_ABSTRACT_LEN:])


def parse_rpc_unix_abstract_address(address: str) -> RpcUnixAbstractAddress:
    if get_rpc_scheme_type(address) != RpcSchemeType.UnixAbstract:
        raise ValueError(f"Invalid Unix Abstract scheme: {address}")
    return _parse_rpc_unix_abstract_address(address)


class Address(NamedTuple):
    address: str
    port: Optional[int]


class RpcIpv4Addresses(NamedTuple):
    """
    Syntax: ``ipv4:address[:port][,address[:port],...]``
    """

    addresses: List[Address]


class RpcIpv6Addresses(NamedTuple):
    """
    Syntax: ``ipv6:address[:port][,address[:port],...]``
    """

    addresses: List[Address]


assert RpcIpv4Addresses != RpcIpv6Addresses, "They must be of different types"
ADDRESS_SEPARATOR = ","


def _parse_rpc_ipv4_addresses(address: str) -> RpcIpv4Addresses:
    assert get_rpc_scheme_type(address) == RpcSchemeType.Ipv4

    addresses = list()
    body = address[SCHEME_IPV4_LEN:]
    for ipv4_address in body.split(ADDRESS_SEPARATOR):
        host_port = parse_ipv4_or_domain_port(ipv4_address)
        host = host_port.host
        port = host_port.port

        if get_ip_address_family(host) != AF_INET:
            raise ValueError(f"Invalid IPv4 address included: {address}")

        addresses.append(Address(host, port))

    return RpcIpv4Addresses(addresses)


def parse_rpc_ipv4_addresses(address: str) -> RpcIpv4Addresses:
    if get_rpc_scheme_type(address) != RpcSchemeType.Ipv4:
        raise ValueError(f"Invalid IPv4 scheme: {address}")
    return _parse_rpc_ipv4_addresses(address)


def _parse_rpc_ipv6_addresses(address: str) -> RpcIpv6Addresses:
    assert get_rpc_scheme_type(address) == RpcSchemeType.Ipv6

    addresses = list()
    body = address[SCHEME_IPV6_LEN:]
    for ipv6_address in body.split(ADDRESS_SEPARATOR):
        host_port = parse_ipv6_port(ipv6_address)
        host = host_port.host
        port = host_port.port

        assert host[0] == OPENING_IPV6
        assert host[-1] == CLOSING_IPV6
        remove_square_bracket_host = host[1:-1]

        if get_ip_address_family(remove_square_bracket_host) != AF_INET6:
            raise ValueError(f"Invalid IPv6 address included: {address}")

        addresses.append(Address(host, port))

    return RpcIpv6Addresses(addresses)


def parse_rpc_ipv6_addresses(address: str) -> RpcIpv6Addresses:
    if get_rpc_scheme_type(address) != RpcSchemeType.Ipv6:
        raise ValueError(f"Invalid IPv6 scheme: {address}")
    return _parse_rpc_ipv6_addresses(address)


UnionRpcAddress = Union[
    RpcDnsAddress,
    RpcUnixAddress,
    RpcUnixAbstractAddress,
    RpcIpv4Addresses,
    RpcIpv6Addresses,
]


def parse_rpc_address(address: str) -> Tuple[RpcSchemeType, UnionRpcAddress]:
    scheme_type = get_rpc_scheme_type(address)
    if scheme_type == RpcSchemeType.Dns:
        return RpcSchemeType.Dns, _parse_rpc_dns_address(address)
    elif scheme_type == RpcSchemeType.Unix:
        return RpcSchemeType.Unix, _parse_rpc_unix_address(address)
    elif scheme_type == RpcSchemeType.UnixAbstract:
        return RpcSchemeType.UnixAbstract, _parse_rpc_unix_abstract_address(address)
    elif scheme_type == RpcSchemeType.Ipv4:
        return RpcSchemeType.Ipv4, _parse_rpc_ipv4_addresses(address)
    elif scheme_type == RpcSchemeType.Ipv6:
        return RpcSchemeType.Ipv6, _parse_rpc_ipv6_addresses(address)
    else:
        assert False, "Inaccessible section"
