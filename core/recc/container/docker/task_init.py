# -*- coding: utf-8 -*-

import os
from typing import Optional
from io import BytesIO
from tarfile import open as tar_open
from recc.archive.tar_archive import file_info
from recc.variables.labels import RECC_CATEGORY_TASK, RECC_VERSION_KEY
from recc.package.requirement_utils import RECC_REQUIREMENTS_MAIN_ARGS
from recc.util.version import version_text
import recc as recc_module

_SCRIPT_PATH = os.path.abspath(__file__)
_SCRIPT_DIR = os.path.dirname(_SCRIPT_PATH)

RECC_MODULE_NAME = recc_module.__name__
RECC_MODULE_INIT_PATH = os.path.abspath(recc_module.__file__)
RECC_MODULE_DIR = os.path.dirname(RECC_MODULE_INIT_PATH)

TASK_GUEST_ROOT_DIR = "/.recc"
TASK_GUEST_WORKSPACE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "workspace")
TASK_GUEST_STORAGE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "storage")
TASK_GUEST_PACKAGE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "package")
TASK_GUEST_CACHE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "cache")
TASK_GUEST_PACKAGE_RECC_DIR = os.path.join(TASK_GUEST_PACKAGE_DIR, RECC_MODULE_NAME)

BASE_IMAGE_NAME = "python"
BASE_IMAGE_TAG = "3.8.9"
BASE_IMAGE_FULLNAME = f"{BASE_IMAGE_NAME}:{BASE_IMAGE_TAG}"
GUEST_GROUP_NAME = "recc"
GUEST_USER_NAME = "recc"

BUILD_CONTEXT_DOCKERFILE_PATH = "/Dockerfile"
BUILD_CONTEXT_RECC_PATH = "/recc"

TASK_INIT_DOCKERFILE_TEMPLATE = f"""
FROM {{base_image}}
MAINTAINER recc

LABEL {RECC_CATEGORY_TASK}
LABEL {RECC_VERSION_KEY}={{recc_version}}

RUN groupadd {{group_name}} && \
    useradd -d "{TASK_GUEST_ROOT_DIR}" -m \
            -g {{group_name}} {{user_name}} && \
    mkdir -p "{TASK_GUEST_ROOT_DIR}" \
             "{TASK_GUEST_WORKSPACE_DIR}" \
             "{TASK_GUEST_STORAGE_DIR}" \
             "{TASK_GUEST_PACKAGE_DIR}" \
             "{TASK_GUEST_CACHE_DIR}" && \
    chown -R {{user_name}}:{{group_name}} "{TASK_GUEST_ROOT_DIR}" && \
    pip3 install {RECC_REQUIREMENTS_MAIN_ARGS}
COPY "{BUILD_CONTEXT_RECC_PATH}" "{TASK_GUEST_PACKAGE_RECC_DIR}"

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
    base_image=BASE_IMAGE_FULLNAME,
    recc_version=version_text,
    group_name=GUEST_GROUP_NAME,
    user_name=GUEST_USER_NAME,
    extra_root_commands: Optional[str] = None,
    extra_user_commands: Optional[str] = None,
) -> bytes:
    root_cmd = "RUN " + extra_root_commands if extra_root_commands else ""
    user_cmd = "RUN " + extra_user_commands if extra_user_commands else ""
    dockerfile = TASK_INIT_DOCKERFILE_TEMPLATE.format(
        base_image=base_image,
        recc_version=recc_version,
        group_name=group_name,
        user_name=user_name,
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

    buffer = BytesIO()
    with tar_open(fileobj=buffer, mode="w") as tar:
        tar.addfile(dockerfile_info, dockerfile_io)
        tar.add(RECC_MODULE_DIR, BUILD_CONTEXT_RECC_PATH, True)
    return buffer.getvalue()
