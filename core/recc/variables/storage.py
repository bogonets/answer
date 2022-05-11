# -*- coding: utf-8 -*-

DEFAULT_STORAGE_HOME_NAME = ".recc"
DEFAULT_STORAGE_GLOBAL_DIR = "/var/recc"

DEFAULT_TEMP_STORAGE_SUFFIX = "recc"
DEFAULT_TEMP_STORAGE_PREFIX = "storage"

# [LocalStorage] first-depth categories.

LOCAL_STORAGE_WORKSPACE_NAME = "workspace"
"""The project's workspace directory.

working/{group}/{project}
"""

LOCAL_STORAGE_TEMPLATE_NAME = "template"
LOCAL_STORAGE_PLUGIN_NAME = "plugin"
LOCAL_STORAGE_DAEMON_NAME = "daemon"
LOCAL_STORAGE_DAEMON_VENV_NAME = "daemon.venv"
LOCAL_STORAGE_DAEMON_WORK_NAME = "daemon.work"
LOCAL_STORAGE_CACHE_NAME = "cache"
LOCAL_STORAGE_PIP_DOWNLOAD_NAME = "pip.download"
LOCAL_STORAGE_TEMP = "temp"

# [TaskStorage] first-depth categories.

TASK_STORAGE_WORKING_NAME = "working"
TASK_STORAGE_TEMPLATE_NAME = "template"
TASK_STORAGE_VENV_NAME = "venv"

STORAGE_SERVICE_TYPE_MINIO = "minio"
STORAGE_REQUEST_TIMEOUT = 60.0
