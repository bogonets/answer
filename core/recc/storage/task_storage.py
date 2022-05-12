# -*- coding: utf-8 -*-

import os
from typing import Dict, KeysView, List, ValuesView

from recc.filesystem.permission import prepare_directory
from recc.storage.sock.sock_path import get_unix_domain_socket_url
from recc.template.lamda_template import LamdaTemplate
from recc.template.manager.lamda_template_key import LamdaTemplateKey
from recc.template.manager.lamda_template_manager import LamdaTemplateManager
from recc.variables.storage import (
    TASK_STORAGE_TEMPLATE_NAME,
    TASK_STORAGE_VENV_NAME,
    TASK_STORAGE_WORKING_NAME,
)


class TaskStorage:
    def __init__(
        self,
        root_dir: str,
        prepare=True,
        refresh_templates=True,
    ):
        self.root = root_dir
        self.working = os.path.join(self.root, TASK_STORAGE_WORKING_NAME)
        self.template = os.path.join(self.root, TASK_STORAGE_TEMPLATE_NAME)
        self.venv = os.path.join(self.root, TASK_STORAGE_VENV_NAME)

        if prepare:
            prepare_directory(self.working)
            prepare_directory(self.template)
            prepare_directory(self.venv)

        self._tm = LamdaTemplateManager(self.template, self.venv)

        if refresh_templates:
            self._tm.refresh()

    @property
    def template_manager(self) -> LamdaTemplateManager:
        return self._tm

    def get_subdirectories(self) -> List[str]:
        """Returns the subdirectories of the workspace"""

        def _filter(name) -> bool:
            return os.path.isdir(os.path.join(self.root, name))

        return list(filter(_filter, os.listdir(self.root)))

    def get_unix_domain_socket_url(self, task_name: str) -> str:
        return get_unix_domain_socket_url(self.root, task_name)

    def refresh_templates(self) -> None:
        self._tm.refresh()

    def get_templates(self) -> Dict[LamdaTemplateKey, LamdaTemplate]:
        assert self._tm is not None
        return self._tm.templates

    def get_template_keys(self) -> KeysView[LamdaTemplateKey]:
        assert self._tm is not None
        return self._tm.keys()

    def get_template_values(self) -> ValuesView[LamdaTemplate]:
        assert self._tm is not None
        return self._tm.values()

    def compress_templates(self) -> bytes:
        assert self._tm is not None
        return self._tm.storage_compressed

    def decompress_templates(self, data: bytes) -> None:
        assert self._tm is not None
        self._tm.decompress_templates(data)
