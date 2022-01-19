# -*- coding: utf-8 -*-

# [CORE] first-depth categories.

CORE_WORKSPACE_NAME = "workspace"
"""The project's workspace directory.

working/{group}/{project}
"""

CORE_TEMPLATE_NAME = "template"
CORE_PLUGIN_NAME = "plugin"
CORE_DAEMON_NAME = "daemon"
CORE_CACHE_NAME = "cache"

CORE_NAMES = (
    CORE_WORKSPACE_NAME,
    CORE_TEMPLATE_NAME,
    CORE_PLUGIN_NAME,
    CORE_DAEMON_NAME,
    CORE_CACHE_NAME,
)

# [WORKSPACE] first-depth categories.

WORKSPACE_WORKING_NAME = "working"
WORKSPACE_TEMPLATE_NAME = "template"
WORKSPACE_VENV_NAME = "venv"

WORKSPACE_NAMES = (
    WORKSPACE_WORKING_NAME,
    WORKSPACE_TEMPLATE_NAME,
    WORKSPACE_VENV_NAME,
)

STORAGE_SERVICE_TYPE_MINIO = "minio"
STORAGE_REQUEST_TIMEOUT = 60.0
