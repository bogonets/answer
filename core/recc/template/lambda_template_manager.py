# -*- coding: utf-8 -*-

import os
import re
from re import Pattern
from io import BytesIO
from tarfile import open as tar_open
from tarfile import TarInfo
from typing import List, Dict, Optional, Iterable, KeysView, ValuesView
from recc.exception.recc_error import ReccDeserializeError, ReccNotFoundError
from recc.package.package_utils import get_module_directory
from recc.file.permission import is_readable_dir
from recc.serializable.json import deserialize_json_file
from recc.template.lambda_template import LambdaTemplate, RuntimeInformation
from recc.template.lambda_template_position import LambdaTemplatePosition
from recc.template.lambda_template_key import LambdaTemplateKey
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment
from recc.variables.template import (
    LAMBDA_TEMPLATE_APP_JSON_SUFFIX_REGEX,
    LAMBDA_TEMPLATE_JSON_SUFFIX_REGEX,
    JSON_SUFFIX_REGEX,
    COMPRESS_IGNORE_PATTERNS,
)
from recc import node as recc_node_module
from recc import node_builtin as recc_node_builtin_module

FIND_APP_JSON_REGEX = re.compile(LAMBDA_TEMPLATE_APP_JSON_SUFFIX_REGEX)
FIND_JSON_REGEX = re.compile(LAMBDA_TEMPLATE_JSON_SUFFIX_REGEX)
REPLACE_JSON_REGEX = re.compile(JSON_SUFFIX_REGEX)
COMPRESS_IGNORE_REGEX = tuple([re.compile(p) for p in COMPRESS_IGNORE_PATTERNS])


def json_to_py_extension(text: str) -> str:
    return REPLACE_JSON_REGEX.sub(".py", text)


def find_app_json_files(directory: str) -> List[str]:
    result = []
    for parent, sub_dirs, files in os.walk(directory):
        for name in files:
            file_cursor = os.path.join(parent, name)
            if FIND_APP_JSON_REGEX.match(file_cursor) is not None:
                result.append(file_cursor)
    return result


def find_json_files(directory: str) -> List[str]:
    result = []
    for parent, sub_dirs, files in os.walk(directory):
        for name in files:
            file_cursor = os.path.join(parent, name)
            if FIND_JSON_REGEX.match(file_cursor) is not None:
                result.append(file_cursor)
    return result


def create_template(
    template_path: str,
    template_directory: Optional[str] = None,
    venv_directory: Optional[str] = None,
) -> LambdaTemplate:
    template = deserialize_json_file(1, template_path, LambdaTemplate)
    if not template.information:
        error_msg = f"Empty template information section: {template_path}"
        raise ReccDeserializeError(error_msg)

    category = template.information.category
    name = template.information.name

    if not category:
        error_msg = f"Empty template category: {template_path}"
        raise ReccDeserializeError(error_msg)

    if not name:
        error_msg = f"Empty template name: {name}"
        raise ReccDeserializeError(error_msg)

    runtime_info = RuntimeInformation()
    runtime_info.template_filename = os.path.basename(template_path)
    runtime_info.template_path = os.path.abspath(template_path)

    script_path: str
    if template.information.script_path:
        _base = os.path.dirname(template_path)
        _path = template.information.script_path
        script_path = os.path.join(_base, _path)
    else:
        script_path = json_to_py_extension(template_path)

    runtime_info.script_filename = os.path.basename(script_path)
    runtime_info.script_path = os.path.abspath(script_path)
    with open(script_path, "r") as script_file:
        runtime_info.script_content = script_file.read()

    runtime_info.optimize = -1
    runtime_info.template_directory = template_directory

    environment = template.information.environment
    if venv_directory and environment and environment.name:
        venv_name = template.information.environment.name
        venv_dir = os.path.join(venv_directory, venv_name)
        runtime_info.venv = AsyncVirtualEnvironment(
            venv_dir, system_site_packages=False
        )

    template.set_runtime_information(runtime_info)

    return template


def create_template_key(
    template: LambdaTemplate,
    position: LambdaTemplatePosition,
) -> LambdaTemplateKey:
    assert template.information is not None
    category = template.information.get_category()
    name = template.information.get_name()
    return LambdaTemplateKey(position, category, name)


def create_templates(
    template_directory: str,
    venv_directory: Optional[str] = None,
) -> List[LambdaTemplate]:
    result = list()
    for file in find_json_files(template_directory):
        result.append(create_template(file, template_directory, venv_directory))
    return result


def create_category_to_names(
    templates: Iterable[LambdaTemplate],
) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = dict()
    for template in templates:
        assert template.information is not None
        category = template.information.get_category()
        name = template.information.get_name()
        if category not in result:
            result[category] = list()
        result[category].append(name)
    return result


def create_template_map(
    builtin_templates: List[LambdaTemplate],
    package_templates: List[LambdaTemplate],
    storage_templates: List[LambdaTemplate],
) -> Dict[LambdaTemplateKey, LambdaTemplate]:
    result = dict()
    for bt in builtin_templates:
        result[create_template_key(bt, LambdaTemplatePosition.Builtin)] = bt
    for pt in package_templates:
        result[create_template_key(pt, LambdaTemplatePosition.Package)] = pt
    for st in storage_templates:
        result[create_template_key(st, LambdaTemplatePosition.Storage)] = st
    return result


def compress_template_directory(
    template_directory: str,
    mode="w",
    ignores=COMPRESS_IGNORE_REGEX,
) -> bytes:
    def _is_dir(name) -> bool:
        return os.path.isdir(os.path.join(template_directory, name))

    def _filter(info: TarInfo) -> Optional[TarInfo]:
        base_name = os.path.basename(info.name)
        for ignore in ignores:
            if isinstance(ignore, Pattern):
                if ignore.match(base_name):
                    return None
            else:
                if re.match(ignore, base_name):
                    return None
        return info

    directories = list(filter(_is_dir, os.listdir(template_directory)))
    file_object = BytesIO()
    with tar_open(fileobj=file_object, mode=mode) as tar:
        for directory in directories:
            path = os.path.join(template_directory, directory)
            tar.add(path, directory, True, filter=_filter)
    return file_object.getvalue()


def decompress_template_directory(extract_directory: str, data: bytes) -> None:
    io_bytes = BytesIO(data)
    with tar_open(fileobj=io_bytes, mode="r") as tar:
        tar.extractall(extract_directory)


class LambdaTemplateManager:
    def __init__(
        self,
        template_directory: Optional[str] = None,
        venv_directory: Optional[str] = None,
    ):
        self._template_directory = template_directory if template_directory else str()
        self._venv_directory = venv_directory if venv_directory else str()

        self._builtin_category_to_names: Dict[str, List[str]] = dict()
        self._package_category_to_names: Dict[str, List[str]] = dict()
        self._storage_category_to_names: Dict[str, List[str]] = dict()
        self._templates: Dict[LambdaTemplateKey, LambdaTemplate] = dict()
        self._storage_compressed = bytes()

    def refresh(self) -> None:
        builtin_dir = get_module_directory(recc_node_builtin_module)
        package_dir = get_module_directory(recc_node_module)
        storage_dir = self._template_directory
        venv_dir = self._venv_directory

        bts = create_templates(builtin_dir, venv_dir)  # Builtin TemplateS -> BTS
        pts = create_templates(package_dir, venv_dir)  # Package TemplateS -> PTS
        sts = create_templates(storage_dir, venv_dir)  # Storage TemplateS -> STS

        self._templates = create_template_map(bts, pts, sts)
        self._builtin_category_to_names = create_category_to_names(bts)
        self._package_category_to_names = create_category_to_names(pts)
        self._storage_category_to_names = create_category_to_names(sts)

        if is_readable_dir(storage_dir):
            self._storage_compressed = compress_template_directory(storage_dir)
        else:
            self._storage_compressed = bytes()

    @property
    def root_dir(self) -> str:
        return self._template_directory

    @property
    def venv_dir(self) -> str:
        return self._venv_directory

    @property
    def builtin_category_to_names(self) -> Dict[str, List[str]]:
        return self._builtin_category_to_names

    @property
    def package_category_to_names(self) -> Dict[str, List[str]]:
        return self._package_category_to_names

    @property
    def storage_category_to_names(self) -> Dict[str, List[str]]:
        return self._storage_category_to_names

    @property
    def templates(self) -> Dict[LambdaTemplateKey, LambdaTemplate]:
        return self._templates

    @property
    def storage_compressed(self) -> bytes:
        return self._storage_compressed

    def keys(self) -> KeysView[LambdaTemplateKey]:
        return self._templates.keys()

    def values(self) -> ValuesView[LambdaTemplate]:
        return self._templates.values()

    def decompress_templates(self, data: bytes) -> None:
        decompress_template_directory(self._template_directory, data)

    def find_template(self, category: str, name: str) -> LambdaTemplate:
        if category in self._storage_category_to_names.keys():
            position = LambdaTemplatePosition.Storage
            category_to_names = self._storage_category_to_names
        elif category in self._package_category_to_names.keys():
            position = LambdaTemplatePosition.Package
            category_to_names = self._package_category_to_names
        elif category in self._builtin_category_to_names.keys():
            position = LambdaTemplatePosition.Builtin
            category_to_names = self._builtin_category_to_names
        else:
            params_msg = f"{category}"
            raise ReccNotFoundError(f"Not found template category: {params_msg}")

        assert category in category_to_names
        if name not in category_to_names[category]:
            params_msg = f"category={category},name={name}"
            raise ReccNotFoundError(f"Not found template: {params_msg}")

        return self._templates[LambdaTemplateKey(position, category, name)]
