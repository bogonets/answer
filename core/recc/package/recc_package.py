# -*- coding: utf-8 -*-

import os
from hashlib import sha256
from io import BytesIO
from tarfile import open as tar_open

import recc as _recc_module
from recc.archive.tar_archive import compress_tar
from recc.package.requirements_utils import RECC_REQUIREMENTS_MAIN_ARG

RECC_MODULE_NAME = _recc_module.__name__
RECC_MODULE_INIT_PATH = os.path.abspath(_recc_module.__file__)
RECC_MODULE_DIR = os.path.dirname(RECC_MODULE_INIT_PATH)
RECC_MODULE_TAR_BYTES = compress_tar(
    RECC_MODULE_DIR, archive_name=RECC_MODULE_NAME, recursive=True
)
RECC_MODULE_TAR_BYTES_SHA256 = sha256(RECC_MODULE_TAR_BYTES).hexdigest()
RECC_REQUIREMENTS_MAIN_SHA256 = sha256(
    bytes(RECC_REQUIREMENTS_MAIN_ARG, encoding="utf-8")
).hexdigest()


def extract_recc_module(path: str) -> None:
    file = BytesIO(RECC_MODULE_TAR_BYTES)
    with tar_open(fileobj=file, mode="r") as tar:
        tar.extractall(path)
