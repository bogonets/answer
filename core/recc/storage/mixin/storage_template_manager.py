# -*- coding: utf-8 -*-

from typing import Optional, Dict, KeysView, ValuesView
from recc.template.lamda_template import LamdaTemplate
from recc.template.manager.lamda_template_key import LamdaTemplateKey
from recc.template.manager.lamda_template_manager import LamdaTemplateManager


class StorageTemplateManagerMixin:

    _tm: LamdaTemplateManager

    def init_template_manager(
        self,
        root: Optional[str] = None,
        venv_directory: Optional[str] = None,
    ) -> None:
        self._tm = LamdaTemplateManager(root, venv_directory)

    def get_template_directory(self) -> str:
        return self._tm.root_dir

    def get_venv_directory(self) -> str:
        return self._tm.venv_dir

    def refresh_templates(self) -> None:
        assert self._tm is not None
        self._tm.refresh()

    def get_template_manager(self) -> LamdaTemplateManager:
        return self._tm

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
