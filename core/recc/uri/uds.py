# -*- coding: utf-8 -*-
# UDS = Unix Domain Socket

from recc.variables.rpc import UNIX_URI_PREFIX, UNIX_ABSTRACT_URI_PREFIX


def is_uds_family(address: str) -> bool:
    if address.startswith(UNIX_URI_PREFIX):
        return True
    if address.startswith(UNIX_ABSTRACT_URI_PREFIX):
        return True
    return False
