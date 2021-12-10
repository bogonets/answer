# -*- coding: utf-8 -*-

import os
from recc.file.directory import prepare_writable_directory


class StorageWorkspaceManagerMixin:

    _workspace_dir: str

    def init_workspace_manager(self, workspace_dir: str) -> None:
        self._workspace_dir = workspace_dir

    def get_workspace_directory(self) -> str:
        return self._workspace_dir

    def prepare_project_dir(self, group_name: str, project_name: str) -> str:
        assert project_name

        group_dir = os.path.join(self._workspace_dir, group_name)
        prepare_writable_directory(group_dir)

        project_dir = os.path.join(group_dir, project_name)
        prepare_writable_directory(project_dir)
        return project_dir

    def get_project_dir(self, group_name: str, project_name: str) -> str:
        assert project_name
        return os.path.join(self._workspace_dir, group_name, project_name)
