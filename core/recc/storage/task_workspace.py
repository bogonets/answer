# -*- coding: utf-8 -*-

import os
from recc.logging.logging import recc_common_logger as logger
from recc.storage.mixin.storage_base import StorageBaseMixin
from recc.storage.mixin.storage_template_manager import StorageTemplateManagerMixin
from recc.storage.sock.sock_path import get_socket_url
from recc.variables.storage import (
    WORKSPACE_WORKING_NAME,
    WORKSPACE_TEMPLATE_NAME,
    WORKSPACE_VENV_NAME,
    WORKSPACE_NAMES,
)


class TaskWorkspace(
    StorageBaseMixin,
    StorageTemplateManagerMixin,
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
            WORKSPACE_NAMES,
            last_temp_candidate=last_temp_candidate,
            read_only=read_only,
            validate=validate,
            prepare=prepare,
        )

        del root_dir
        selected_root_dir = self.get_root_directory()

        template_dir = os.path.join(selected_root_dir, WORKSPACE_TEMPLATE_NAME)
        venv_dir = os.path.join(selected_root_dir, WORKSPACE_VENV_NAME)
        self.init_template_manager(template_dir, venv_dir)

        if refresh_templates:
            self.refresh_templates()

    def get_working_dir(self) -> str:
        return os.path.join(self.get_root_directory(), WORKSPACE_WORKING_NAME)

    def get_socket_url(self, task_name: str) -> str:
        return get_socket_url(self.get_root_directory(), task_name)

    def change_working_directory(self) -> None:
        working_dir = self.get_working_dir()
        if not os.path.isdir(working_dir):
            logger.warning(f"A working directory is not a 'directory': {working_dir}")
            return

        try:
            os.chdir(self.get_working_dir())
        except BaseException as e:
            logger.exception(e)
        else:
            logger.info(f"The working directory has changed: {working_dir}")
