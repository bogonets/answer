# -*- coding: utf-8 -*-

import os
from typing import List, Union
from tempfile import mkdtemp
from recc.file.permission import is_readable_dir
from recc.file.path_utils import HOME_DIR
from recc.file.directory import prepare_writable_directory
from recc.template.template_manager import TemplateManagerMixin
from recc.variables.storage_names import (
    WORKSPACE_NAME,
    PYTHON_NAME,
    VENV_NAME,
    GLOBAL_WORKSPACE_NAME,
)
from recc.variables.database import ANONYMOUS_GROUP_NAME

ANSWER_HOME = os.path.join(HOME_DIR, ".answer")
ANSWER_HOME_STORAGE_DIR = os.path.join(ANSWER_HOME, "core.storage")
GLOBAL_STORAGE_DIR = "/usr/local/c2core/storage"


def find_available_storage_root(dirs: Union[str, List[str]]) -> str:
    """
    :param dirs:
        List of candidate directories.
    """

    candidates = []
    if isinstance(dirs, str):
        candidates += [dirs]
    elif isinstance(dirs, list):
        candidates += dirs
    candidates += [ANSWER_HOME_STORAGE_DIR, GLOBAL_STORAGE_DIR]

    for cursor in candidates:
        if cursor and is_readable_dir(cursor):
            return cursor

    raise FileNotFoundError("Not found storage directory.")


class AsyncStorageManager(TemplateManagerMixin):
    def __init__(
        self,
        root_dir: str,
        workspace_name=WORKSPACE_NAME,
        template_name=PYTHON_NAME,
        venv_name=VENV_NAME,
        global_workspace_name=GLOBAL_WORKSPACE_NAME,
    ):
        try:
            storage_dir = find_available_storage_root(root_dir)
            self._prepare_storage(storage_dir)
        except:  # noqa
            # Registers a temporary directory as the last candidate.
            storage_dir = mkdtemp(suffix="recc", prefix="storage")
            self._prepare_storage(storage_dir)

        prepare_writable_directory(os.path.join(storage_dir, workspace_name))
        prepare_writable_directory(os.path.join(storage_dir, template_name))
        prepare_writable_directory(os.path.join(storage_dir, global_workspace_name))

        self._root_directory = os.path.abspath(storage_dir)
        self._workspace_name = workspace_name
        self._template_name = template_name
        self._venv_name = venv_name
        self._global_workspace_name = global_workspace_name

        template_dir = os.path.join(self._root_directory, template_name)
        venv_dir = os.path.join(self._root_directory, venv_name)
        self.init_template_manager(template_dir, venv_dir)

    @staticmethod
    def _prepare_storage(root_dir: str) -> None:
        candidate_directory = find_available_storage_root(root_dir)
        prepare_writable_directory(candidate_directory)

    @property
    def root(self) -> str:
        return self._root_directory

    @property
    def workspace_dir(self) -> str:
        return os.path.join(self._root_directory, self._workspace_name)

    @property
    def template_dir(self) -> str:
        return os.path.join(self._root_directory, self._template_name)

    @property
    def venv_dir(self) -> str:
        return os.path.join(self._root_directory, self._venv_name)

    @property
    def global_workspace_dir(self) -> str:
        return os.path.join(self._root_directory, self._global_workspace_name)

    def prepare_workspace_dir(self, group_name: str, project_name: str) -> str:
        if group_name == ANONYMOUS_GROUP_NAME:
            group_dir = self.global_workspace_dir
        else:
            group_dir = os.path.join(self.workspace_dir, group_name)
            prepare_writable_directory(group_dir)

        project_dir = os.path.join(group_dir, project_name)
        prepare_writable_directory(project_dir)
        return project_dir
