# -*- coding: utf-8 -*-

import os
from typing import List
from pathlib import Path
from recc.storage.mixin.storage_base import StorageBaseMixin
from recc.storage.mixin.storage_template_manager import StorageTemplateManagerMixin
from recc.storage.mixin.storage_workspace_manager import StorageWorkspaceManagerMixin
from recc.variables.storage import (
    CORE_WORKSPACE_NAME,
    CORE_TEMPLATE_NAME,
    CORE_PLUGIN_NAME,
    CORE_DAEMON_NAME,
    CORE_CACHE_NAME,
    CORE_NAMES,
)


class LocalStorage(
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
            root_dir=root_dir,
            subdir_names=CORE_NAMES,
            last_temp_candidate=last_temp_candidate,
            read_only=read_only,
            validate=validate,
            prepare=prepare,
        )

        del root_dir
        selected_root_dir = self.get_root_directory()

        working_dir = os.path.join(selected_root_dir, CORE_WORKSPACE_NAME)
        self.init_workspace_manager(working_dir)

        template_dir = os.path.join(selected_root_dir, CORE_TEMPLATE_NAME)
        self.init_template_manager(template_dir, venv_directory=None)

        if refresh_templates:
            self.refresh_templates()

        self.plugin = Path(os.path.join(selected_root_dir, CORE_PLUGIN_NAME))
        self.daemon = Path(os.path.join(selected_root_dir, CORE_DAEMON_NAME))
        self.cache = Path(os.path.join(selected_root_dir, CORE_CACHE_NAME))

    def find_plugin_dirs(self) -> List[Path]:
        result: List[Path] = list()
        for file in self.plugin.iterdir():
            if file.is_dir():
                result.append(file)
        return result

    def find_daemon_dirs(self) -> List[Path]:
        result: List[Path] = list()
        for file in self.daemon.iterdir():
            if file.is_dir():
                result.append(file)
        return result
