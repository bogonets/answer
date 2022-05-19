# -*- coding: utf-8 -*-

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional

from recc.filesystem.permission import prepare_directory
from recc.template.lamda_template import LamdaTemplate
from recc.template.manager.lamda_template_key import LamdaTemplateKey
from recc.template.manager.lamda_template_manager import LamdaTemplateManager
from recc.variables.storage import (
    LOCAL_STORAGE_CACHE_NAME,
    LOCAL_STORAGE_DAEMON_NAME,
    LOCAL_STORAGE_DAEMON_VENV_NAME,
    LOCAL_STORAGE_DAEMON_WORK_NAME,
    LOCAL_STORAGE_PIP_DOWNLOAD_NAME,
    LOCAL_STORAGE_PLUGIN_NAME,
    LOCAL_STORAGE_TEMP,
    LOCAL_STORAGE_TEMPLATE_NAME,
    LOCAL_STORAGE_WORKSPACE_NAME,
)


class LocalStorage:
    def __init__(
        self,
        root_dir: str,
        prepare=True,
        refresh_templates=True,
    ):
        self.root = root_dir
        self.workspace = os.path.join(self.root, LOCAL_STORAGE_WORKSPACE_NAME)
        self.template = os.path.join(self.root, LOCAL_STORAGE_TEMPLATE_NAME)
        self.plugin = os.path.join(self.root, LOCAL_STORAGE_PLUGIN_NAME)
        self.daemon = os.path.join(self.root, LOCAL_STORAGE_DAEMON_NAME)
        self.daemon_venv = os.path.join(self.root, LOCAL_STORAGE_DAEMON_VENV_NAME)
        self.daemon_work = os.path.join(self.root, LOCAL_STORAGE_DAEMON_WORK_NAME)
        self.cache = os.path.join(self.root, LOCAL_STORAGE_CACHE_NAME)
        self.pip_download = os.path.join(self.root, LOCAL_STORAGE_PIP_DOWNLOAD_NAME)
        self.temp = os.path.join(self.root, LOCAL_STORAGE_TEMP)

        if prepare:
            prepare_directory(self.root)
            prepare_directory(self.workspace)
            prepare_directory(self.template)
            prepare_directory(self.plugin)
            prepare_directory(self.daemon)
            prepare_directory(self.daemon_venv)
            prepare_directory(self.daemon_work)
            prepare_directory(self.cache)
            prepare_directory(self.pip_download)
            prepare_directory(self.temp)

        self._tm = LamdaTemplateManager(self.template, venv_directory=None)

        if refresh_templates:
            self._tm.refresh()

    @property
    def template_manager(self) -> LamdaTemplateManager:
        return self._tm

    def prepare_project_directory(self, group: str, project: str) -> str:
        group_dir = os.path.join(self.workspace, group)
        prepare_directory(group_dir)

        project_dir = os.path.join(group_dir, project)
        prepare_directory(project_dir)

        return project_dir

    def get_project_directory(self, group: str, project: str) -> str:
        return os.path.join(self.workspace, group, project)

    def get_template_directory(self) -> str:
        return self._tm.root_dir

    def refresh_templates(self) -> None:
        assert self._tm is not None
        self._tm.refresh()

    def get_templates(self) -> Dict[LamdaTemplateKey, LamdaTemplate]:
        assert self._tm is not None
        return self._tm.templates

    def compress_templates(self) -> bytes:
        assert self._tm is not None
        return self._tm.storage_compressed

    def decompress_templates(self, data: bytes) -> None:
        assert self._tm is not None
        self._tm.decompress_templates(data)

    def create_temporary_directory(
        self,
        suffix: Optional[str] = None,
        prefix: Optional[str] = None,
    ):
        return TemporaryDirectory(suffix, prefix, self.temp)
