# -*- coding: utf-8 -*-

_1KB = 1024
_1MB = _1KB * 1024
_1GB = _1MB * 1024

MAX_SEND_MESSAGE_LENGTH = _1GB
MAX_RECEIVE_MESSAGE_LENGTH = _1GB

DEFAULT_GRPC_OPTIONS = [
    ("grpc.max_send_message_length", MAX_SEND_MESSAGE_LENGTH),
    ("grpc.max_receive_message_length", MAX_RECEIVE_MESSAGE_LENGTH),
]
