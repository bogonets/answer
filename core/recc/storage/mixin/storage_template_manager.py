# -*- coding: utf-8 -*-

from typing import Optional, Dict, KeysView, ValuesView
from recc.template.lambda_template import LambdaTemplate
from recc.template.lambda_template_key import LambdaTemplateKey
from recc.template.lambda_template_manager import LambdaTemplateManager


class StorageTemplateManagerMixin:

    _tm: LambdaTemplateManager

    def init_template_manager(
        self,
        root: Optional[str] = None,
        venv_directory: Optional[str] = None,
    ) -> None:
        self._tm = LambdaTemplateManager(root, venv_directory)

    def get_template_directory(self) -> str:
        return self._tm.root_dir

    def get_venv_directory(self) -> str:
        return self._tm.venv_dir

    def refresh_templates(self) -> None:
        assert self._tm is not None
        self._tm.refresh()

    def get_template_manager(self) -> LambdaTemplateManager:
        return self._tm

    def get_templates(self) -> Dict[LambdaTemplateKey, LambdaTemplate]:
        assert self._tm is not None
        return self._tm.templates

    def get_template_keys(self) -> KeysView[LambdaTemplateKey]:
        assert self._tm is not None
        return self._tm.keys()

    def get_template_values(self) -> ValuesView[LambdaTemplate]:
        assert self._tm is not None
        return self._tm.values()

    def compress_templates(self) -> bytes:
        assert self._tm is not None
        return self._tm.storage_compressed

    def decompress_templates(self, data: bytes) -> None:
        assert self._tm is not None
        self._tm.decompress_templates(data)
