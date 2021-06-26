# -*- coding: utf-8 -*-

import os
from typing import Optional
from io import BytesIO
from hashlib import sha256
from tarfile import open as tar_open
from recc.archive.tar_archive import compress_tar, file_info
from recc.variables.labels import (
    RECC_CATEGORY_IMAGE,
    RECC_IMAGE_VERSION_KEY,
    RECC_IMAGE_SHA256_KEY,
)
from recc.package.requirement_utils import RECC_REQUIREMENTS_MAIN_ARG
from recc.util.version import version_text
import recc as recc_module

BASE_IMAGE_NAME = "python"
BASE_IMAGE_TAG = "3.8.9"
BASE_IMAGE_FULLNAME = f"{BASE_IMAGE_NAME}:{BASE_IMAGE_TAG}"
GUEST_GROUP_NAME = "recc"
GUEST_USER_NAME = "recc"

BUILD_CONTEXT_BUILD_PATH = "/"
BUILD_CONTEXT_DOCKERFILE_PATH = "/Dockerfile"
BUILD_CONTEXT_RECC_PATH = "/recc.tar"

RECC_MODULE_NAME = recc_module.__name__
RECC_MODULE_INIT_PATH = os.path.abspath(recc_module.__file__)
RECC_MODULE_DIR = os.path.dirname(RECC_MODULE_INIT_PATH)
RECC_MODULE_TAR_BYTES = compress_tar(
    RECC_MODULE_DIR, archive_name=RECC_MODULE_NAME, recursive=True
)
RECC_MODULE_TAR_BYTES_SHA256 = sha256(RECC_MODULE_TAR_BYTES).hexdigest()

TASK_GUEST_ROOT_DIR = "/.recc"
TASK_GUEST_WORKSPACE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "workspace")
TASK_GUEST_STORAGE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "storage")
TASK_GUEST_PACKAGE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "package")
TASK_GUEST_CACHE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "cache")

TASK_INIT_DOCKERFILE_TEMPLATE = f"""
FROM {{base_image}}
MAINTAINER recc

LABEL {RECC_CATEGORY_IMAGE}
LABEL {RECC_IMAGE_VERSION_KEY}={{recc_version}}
LABEL {RECC_IMAGE_SHA256_KEY}={RECC_MODULE_TAR_BYTES_SHA256}

RUN groupadd {{group_name}} && \
    useradd -d "{TASK_GUEST_ROOT_DIR}" -m \
            -g {{group_name}} {{user_name}} && \
    mkdir -p "{TASK_GUEST_ROOT_DIR}" \
             "{TASK_GUEST_WORKSPACE_DIR}" \
             "{TASK_GUEST_STORAGE_DIR}" \
             "{TASK_GUEST_PACKAGE_DIR}" \
             "{TASK_GUEST_CACHE_DIR}" && \
    chown -R {{user_name}}:{{group_name}} "{TASK_GUEST_ROOT_DIR}" && \
    pip3 install {RECC_REQUIREMENTS_MAIN_ARG}

ADD "{BUILD_CONTEXT_RECC_PATH}" "{TASK_GUEST_PACKAGE_DIR}"

{{extra_root_commands}}

ENV RECC_USER {{user_name}}
ENV RECC_GROUP {{group_name}}
ENV RECC_WORKSPACE_DIR "{TASK_GUEST_WORKSPACE_DIR}"
ENV RECC_STORAGE_DIR "{TASK_GUEST_STORAGE_DIR}"
ENV RECC_PACKAGE_DIR "{TASK_GUEST_PACKAGE_DIR}"
ENV RECC_CACHE_DIR "{TASK_GUEST_CACHE_DIR}"
ENV PYTHONPATH "{TASK_GUEST_PACKAGE_DIR}:$PYTHONPATH"

WORKDIR "{TASK_GUEST_WORKSPACE_DIR}"
USER {{user_name}}

{{extra_user_commands}}

ENTRYPOINT ["python3", "-m", "recc"]
"""


def get_compressed_task_dockerfile_tar(
    base_image: Optional[str] = None,
    recc_version: Optional[str] = None,
    group_name: Optional[str] = None,
    user_name: Optional[str] = None,
    extra_root_commands: Optional[str] = None,
    extra_user_commands: Optional[str] = None,
) -> bytes:
    img = base_image if base_image else BASE_IMAGE_FULLNAME
    ver = recc_version if recc_version else version_text
    group = group_name if group_name else GUEST_GROUP_NAME
    user = user_name if user_name else GUEST_USER_NAME
    root_cmd = "RUN " + extra_root_commands if extra_root_commands else ""
    user_cmd = "RUN " + extra_user_commands if extra_user_commands else ""
    dockerfile = TASK_INIT_DOCKERFILE_TEMPLATE.format(
        base_image=img,
        recc_version=ver,
        group_name=group,
        user_name=user,
        extra_root_commands=root_cmd,
        extra_user_commands=user_cmd,
    )
    dockerfile_bytes = dockerfile.encode("utf-8")
    dockerfile_info = file_info(
        BUILD_CONTEXT_DOCKERFILE_PATH,
        len(dockerfile_bytes),
        0o544,
    )
    dockerfile_io = BytesIO(dockerfile_bytes)

    recc_tar_bytes = RECC_MODULE_TAR_BYTES
    recc_tar_info = file_info(
        BUILD_CONTEXT_RECC_PATH,
        len(recc_tar_bytes),
        0o544,
    )
    recc_tar_io = BytesIO(recc_tar_bytes)

    buffer = BytesIO()
    with tar_open(fileobj=buffer, mode="w") as tar:
        tar.addfile(dockerfile_info, dockerfile_io)
        tar.addfile(recc_tar_info, recc_tar_io)
    return buffer.getvalue()
