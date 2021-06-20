# -*- coding: utf-8 -*-

import os
from tempfile import mkdtemp
from typing import List
from recc.variables.storage_names import WORKING_NAME, PYTHON_NAME, VENV_NAME
from recc.file.directory import prepare_writable_directory
from recc.template.template_manager import TemplateManagerMixin


class AsyncWorkspace(TemplateManagerMixin):
    def __init__(
        self,
        root_dir: str,
        working_name=WORKING_NAME,
        template_name=PYTHON_NAME,
        venv_name=VENV_NAME,
    ):
        try:
            enable_temporary = False
            workspace_dir = root_dir
            prepare_writable_directory(workspace_dir)
        except:  # noqa
            # Registers a temporary directory as the last candidate.
            enable_temporary = True
            workspace_dir = mkdtemp(suffix="recc", prefix="workspace")
            prepare_writable_directory(workspace_dir)

        prepare_writable_directory(os.path.join(workspace_dir, working_name))
        prepare_writable_directory(os.path.join(workspace_dir, template_name))
        prepare_writable_directory(os.path.join(workspace_dir, venv_name))

        self._enable_temporary = enable_temporary
        self._root_directory = os.path.abspath(workspace_dir)
        self._working_name = working_name
        self._template_name = template_name
        self._venv_name = venv_name

        template_dir = os.path.join(self._root_directory, template_name)
        venv_dir = os.path.join(self._root_directory, venv_name)
        self.init_template_manager(template_dir, venv_dir)

    @property
    def root(self) -> str:
        return self._root_directory

    @property
    def working_dir(self) -> str:
        return os.path.join(self._root_directory, self._working_name)

    @property
    def template_dir(self) -> str:
        return os.path.join(self._root_directory, self._template_name)

    @property
    def venv_dir(self) -> str:
        return os.path.join(self._root_directory, self._venv_name)

    def get_workspace_subdir(self) -> List[str]:
        """Returns the subdirectories of the workspace."""

        def _filter(name) -> bool:
            return os.path.isdir(os.path.join(self.root, name))

        return list(filter(_filter, os.listdir(self.root)))
