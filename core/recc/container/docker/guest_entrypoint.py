# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import open as tar_open
from recc.variables.task_guest import TASK_GUEST_ENTRYPOINT

SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
GUEST_ENTRYPOINT_SCRIPT_NAME = "guest_entrypoint.sh"
GUEST_ENTRYPOINT_SCRIPT_PATH = os.path.join(SCRIPT_DIR, GUEST_ENTRYPOINT_SCRIPT_NAME)


def compress_guest_entrypoint_script_tar() -> bytes:
    file_object = BytesIO()
    with tar_open(fileobj=file_object, mode="w") as tar:
        tar.add(TASK_GUEST_ENTRYPOINT, GUEST_ENTRYPOINT_SCRIPT_PATH)
    return file_object.getvalue()
