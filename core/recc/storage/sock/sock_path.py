# -*- coding: utf-8 -*-

import os
from recc.rule.naming_socket import naming_socket
from recc.variables.rpc import UNIX_URI_PREFIX

_TASK_SOCKET_URL_PREFIX = f"{UNIX_URI_PREFIX}//"


def get_socket_url(directory: str, task_name: str) -> str:
    """Get a Unix Domain Socket URL for RPC.

    .. warning::
        In the directory shared by Docker Volume,
        socket file cannot be created if host and guest have different OS.
    """

    assert directory
    assert task_name

    suffix = os.path.join(directory, naming_socket(task_name))
    return _TASK_SOCKET_URL_PREFIX + suffix
