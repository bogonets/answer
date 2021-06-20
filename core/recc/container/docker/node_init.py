# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import open as tar_open
from recc.archive.tar_archive import add_dirs
from recc.variables.task_guest import (
    TASK_GUEST_PACKAGE_DIR,
)

RECC_MODULE_NAME = "recc"
RECC_MODULE_INIT_PATH = os.path.abspath(__import__(RECC_MODULE_NAME).__file__)
RECC_MODULE_DIR = os.path.dirname(RECC_MODULE_INIT_PATH)
NODE_GUEST_RECC_PATH = os.path.join(TASK_GUEST_PACKAGE_DIR, RECC_MODULE_NAME)


def compress_node_init_tar() -> bytes:
    file_object = BytesIO()
    with tar_open(fileobj=file_object, mode="w") as tar:
        add_dirs(tar, TASK_GUEST_PACKAGE_DIR)
        tar.add(RECC_MODULE_DIR, NODE_GUEST_RECC_PATH, True)
    return file_object.getvalue()


COMPRESS_NODE_INIT_TAR_BYTES = compress_node_init_tar()
