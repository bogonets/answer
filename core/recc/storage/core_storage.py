# -*- coding: utf-8 -*-

import os
from recc.storage.sock.sock_path import get_socket_url
from recc.storage.mixin.storage_base import StorageBaseMixin
from recc.storage.mixin.storage_template_manager import StorageTemplateManagerMixin
from recc.storage.mixin.storage_workspace_manager import StorageWorkspaceManagerMixin
from recc.variables.storage import (
    CORE_WORKSPACE_NAME,
    CORE_WORKSPACE_GLOBAL_NAME,
    CORE_TEMPLATE_NAME,
    CORE_NAMES,
)


class CoreStorage(
    StorageBaseMixin,
    StorageTemplateManagerMixin,
    StorageWorkspaceManagerMixin,
):
    def __init__(
        self,
        root_dir: str,
        last_temp_candidate=True,
        read_only=False,
        validate=True,
        prepare=True,
        refresh_templates=True,
    ):
        self.init_storage(
            root_dir,
            CORE_NAMES,
            last_temp_candidate=last_temp_candidate,
            read_only=read_only,
            validate=validate,
            prepare=prepare,
        )

        del root_dir
        selected_root_dir = self.get_root_directory()

        working_dir = os.path.join(selected_root_dir, CORE_WORKSPACE_NAME)
        working_global_dir = os.path.join(selected_root_dir, CORE_WORKSPACE_GLOBAL_NAME)
        self.init_workspace_manager(working_dir, working_global_dir)

        template_dir = os.path.join(selected_root_dir, CORE_TEMPLATE_NAME)
        self.init_template_manager(template_dir, venv_directory=None)

        if refresh_templates:
            self.refresh_templates()

    def get_socket_url(self, group_name: str, project_name: str, task_name: str) -> str:
        prefix = self.get_project_dir(group_name, project_name)
        return get_socket_url(prefix, task_name)
