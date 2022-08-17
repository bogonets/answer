# -*- coding: utf-8 -*-

from recc.variables.rpc import UNIX_ABSTRACT_URI_PREFIX, UNIX_URI_PREFIX


def is_uds_family(address: str) -> bool:
    """
    Make sure it is a Unix Domain Socket (UDS) address.
    """
    if address.startswith(UNIX_URI_PREFIX):
        return True
    if address.startswith(UNIX_ABSTRACT_URI_PREFIX):
        return True
    return False
