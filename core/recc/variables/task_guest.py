# -*- coding: utf-8 -*-

import os

TASK_GUEST_USER = "answer"
TASK_GUEST_GROUP = "answer"

TASK_GUEST_ROOT_DIR = "/.answer"
TASK_GUEST_WORKSPACE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "workspace")
TASK_GUEST_CACHE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "cache")
TASK_GUEST_PACKAGE_DIR = os.path.join(TASK_GUEST_ROOT_DIR, "package")
