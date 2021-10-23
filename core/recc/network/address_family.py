# -*- coding: utf-8 -*-

from ipaddress import ip_address, IPv4Address
from socket import AF_INET, AF_INET6


def get_ip_address_family(address: str) -> int:
    return AF_INET if type(ip_address(address)) is IPv4Address else AF_INET6


def is_ip_address(address: str) -> bool:
    try:
        ip_address(address)
    except ValueError:
        return False
    else:
        return True
