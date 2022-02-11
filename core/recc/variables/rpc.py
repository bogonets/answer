# -*- coding: utf-8 -*-

from recc.variables.port import DEFAULT_TASK_RPC_PORT, DEFAULT_DAEMON_PORT

_1KB = 1024
_1MB = _1KB * 1024
_1GB = _1MB * 1024

MAX_SEND_MESSAGE_LENGTH = _1GB
MAX_RECEIVE_MESSAGE_LENGTH = _1GB

DEFAULT_GRPC_OPTIONS = [
    ("grpc.max_send_message_length", MAX_SEND_MESSAGE_LENGTH),
    ("grpc.max_receive_message_length", MAX_RECEIVE_MESSAGE_LENGTH),
]

ACCEPTED_UDS_PORT_NUMBER = 1
"""The accepted UDS(Unix Domain Socket) port number is fixed as `1`.

Reference:
 - File: grpc/src/core/lib/iomgr/unix_sockets_posix.cc
 - Func: grpc_resolve_unix_domain_address
"""

UNIX_URI_PREFIX = "unix:"
"""Prefix of UDS(Unix Domain Socket).

Reference:
 - Site: `gRPC Name Resolution <https://grpc.github.io/grpc/cpp/md_doc_naming.html>`_
 - File: grpc/src/core/ext/transport/chttp2/server/chttp2_server.cc
"""

UNIX_ABSTRACT_URI_PREFIX = "unix-abstract:"
"""Prefix of UDS(Unix Domain Socket) in abstract namespace.

Reference:
 - Site: `gRPC Name Resolution <https://grpc.github.io/grpc/cpp/md_doc_naming.html>`_
 - File: grpc/src/core/ext/transport/chttp2/server/chttp2_server.cc
"""

DEFAULT_RPC_BIND = "[::]"
DEFAULT_RPC_PORT = DEFAULT_TASK_RPC_PORT
DEFAULT_RPC_ADDRESS = f"{DEFAULT_RPC_BIND}:{DEFAULT_RPC_PORT}"

DEFAULT_DAEMON_BIND = "[::]"
DEFAULT_DAEMON_PORT = DEFAULT_DAEMON_PORT
DEFAULT_DAEMON_ADDRESS = f"{DEFAULT_DAEMON_BIND}:{DEFAULT_DAEMON_PORT}"

DEFAULT_WAIT_TASK_INTERVAL = 1.0
DEFAULT_WAIT_TASK_TIMEOUT = 8.0
DEFAULT_WAIT_TASK_RETRIES = 10

REGISTER_KEY_RSA_SIZE = 2048

DEFAULT_HEARTBEAT_TIMEOUT = 5.0
DEFAULT_PACKET_MAX_SIZE = 100 * 1024 * 1024

DEFAULT_PICKLE_PROTOCOL_VERSION = 5
DEFAULT_PICKLE_ENCODING = "ASCII"

REGISTER_ANSWER_KEY_MIN_SM_SIZE = "min_sm_size"
REGISTER_ANSWER_KEY_MIN_SM_BYTE = "min_sm_byte"
