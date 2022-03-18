# -*- coding: utf-8 -*-

CONTAINER_TYPE_DOCKER = "docker"
CONTAINER_TYPE_SWARM = "swarm"
CONTAINER_TYPE_KUBERNETES = "kubernetes"

DOCKER_SOCK_LOCAL_BASE_URL = "unix://var/run/docker.sock"

BASE_IMAGE_NAME = "python"
BASE_IMAGE_TAG = "3.9.11"
BASE_IMAGE_FULLNAME = f"{BASE_IMAGE_NAME}:{BASE_IMAGE_TAG}"

TASK_IMAGE_NAME = "recc-task-image"
TASK_IMAGE_LATEST_FULLNAME = f"{TASK_IMAGE_NAME}:latest"

GUEST_GROUP_NAME = "recc"
GUEST_USER_NAME = "recc"

BUILD_CONTEXT_BUILD_PATH = "/"
BUILD_CONTEXT_DOCKERFILE_PATH = "/Dockerfile"
BUILD_CONTEXT_RECC_PATH = "/recc.tar"

TASK_GUEST_WORKSPACE_DIR = "/.recc"
TASK_GUEST_PACKAGE_DIR = "/.recc-package"
TASK_GUEST_CACHE_DIR = "/.recc-cache"

DEFAULT_RESTART_COUNT = 5
DEFAULT_TIME_ZONE = "Asia/Seoul"
