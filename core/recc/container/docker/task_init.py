# -*- coding: utf-8 -*-

import os
from io import BytesIO
from tarfile import TarFile
from tarfile import open as tar_open
from recc.archive.tar_archive import file_info, dir_info
import recc as recc_module

_SCRIPT_PATH = os.path.abspath(__file__)
_SCRIPT_DIR = os.path.dirname(_SCRIPT_PATH)

GUEST_ENTRYPOINT_SCRIPT_NAME = "task_entrypoint.sh"
GUEST_ENTRYPOINT_SCRIPT_PATH = os.path.join(_SCRIPT_DIR, GUEST_ENTRYPOINT_SCRIPT_NAME)

RECC_MODULE_NAME = recc_module.__name__
RECC_MODULE_INIT_PATH = os.path.abspath(recc_module.__file__)
RECC_MODULE_DIR = os.path.dirname(RECC_MODULE_INIT_PATH)

TASK_GUEST_WORKSPACE_DIR = "/.recc"
TASK_GUEST_PACKAGE_DIR = "/.recc-package"
TASK_GUEST_ENTRYPOINT = "/.recc-entrypoint"
TASK_GUEST_RECC_PATH = os.path.join(TASK_GUEST_PACKAGE_DIR, RECC_MODULE_NAME)


def get_entrypoint_script_bytes() -> bytes:
    with open(GUEST_ENTRYPOINT_SCRIPT_PATH, mode="rb") as f:
        return f.read()


def add_entrypoint_script(tar: TarFile) -> None:
    entrypoint_script = get_entrypoint_script_bytes()
    info = file_info(TASK_GUEST_ENTRYPOINT, len(entrypoint_script))
    tar.addfile(info, BytesIO(entrypoint_script))


def compress_task_init_tar() -> bytes:
    buffer = BytesIO()
    with tar_open(fileobj=buffer, mode="w") as tar:
        tar.addfile(dir_info(TASK_GUEST_WORKSPACE_DIR))
        tar.addfile(dir_info(TASK_GUEST_PACKAGE_DIR))
        add_entrypoint_script(tar)
        tar.add(RECC_MODULE_DIR, TASK_GUEST_RECC_PATH, True)
    return buffer.getvalue()


TASK_INIT_TAR_BYTES = compress_task_init_tar()
