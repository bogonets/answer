# -*- coding: utf-8 -*-

# [CORE] first-depth categories.

CORE_WORKSPACE_NAME = "workspace"
"""The project's workspace directory.

working/{group}/{project}
"""

CORE_WORKSPACE_GLOBAL_NAME = "workspace.global"
"""The global project's workspace directory.

working.global/{project}
"""

CORE_TEMPLATE_NAME = "template"

CORE_NAMES = (
    CORE_WORKSPACE_NAME,
    CORE_WORKSPACE_GLOBAL_NAME,
    CORE_TEMPLATE_NAME,
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
