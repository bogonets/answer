# -*- coding: utf-8 -*-

import os
import re
from enum import Enum
from re import Pattern
from io import BytesIO
from tarfile import open as tar_open
from tarfile import TarInfo
from typing import List, Dict, Optional, Tuple, Iterable, KeysView, ValuesView
from recc.exception.recc_error import ReccDeserializeError, ReccNotFoundError
from recc.package.package_utils import get_module_directory
from recc.file.permission import is_readable_dir
from recc.serializable.json import deserialize_json_file
from recc.template.template import Template, RuntimeInformation
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment
from recc import node as recc_node_module
from recc import node_builtin as recc_node_builtin_module

TEMPLATE_KEY_DELIMITER = "/"
FIND_APP_JSON_REGEX = re.compile(r"(?i).*\.app\.json$")
FIND_JSON_REGEX = re.compile(r"(?i).*\.json$")
REPLACE_JSON_REGEX = re.compile(r"\.json$")

COMPRESS_IGNORE_PATTERNS = (
    r"\.DS_Store",
    r"\.git",
    r"__pycache__",
    r".*\.py[cod]",
)
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


class TemplatePosition(Enum):
    Builtin = 0
    Package = 1
    Storage = 2


def make_template_key(
    position: TemplatePosition,
    category: str,
    name: str,
    delimiter: str = TEMPLATE_KEY_DELIMITER,
) -> str:
    return position.name + delimiter + category + delimiter + name


class TemplateKey:

    position: TemplatePosition
    category: str
    name: str

    def __init__(
        self,
        position: TemplatePosition,
        category: str,
        name: str,
    ):
        self.position = position
        self.category = category
        self.name = name

    def to_tuple(self) -> Tuple[TemplatePosition, str, str]:
        return self.position, self.category, self.name

    def __str__(self) -> str:
        return make_template_key(self.position, self.category, self.name)

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)


def create_template(
    template_path: str,
    template_directory: Optional[str] = None,
    venv_directory: Optional[str] = None,
) -> Template:
    template = deserialize_json_file(1, template_path, Template)
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


def create_template_key(template: Template, position: TemplatePosition) -> TemplateKey:
    assert template.information is not None
    category = template.information.get_category()
    name = template.information.get_name()
    return TemplateKey(position, category, name)


def create_templates(
    template_directory: str,
    venv_directory: Optional[str] = None,
) -> List[Template]:
    result = list()
    for file in find_json_files(template_directory):
        result.append(create_template(file, template_directory, venv_directory))
    return result


def create_category_to_names(templates: Iterable[Template]) -> Dict[str, List[str]]:
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
    builtin_templates: List[Template],
    package_templates: List[Template],
    storage_templates: List[Template],
) -> Dict[TemplateKey, Template]:
    result = dict()
    for bt in builtin_templates:
        result[create_template_key(bt, TemplatePosition.Builtin)] = bt
    for pt in package_templates:
        result[create_template_key(pt, TemplatePosition.Package)] = pt
    for st in storage_templates:
        result[create_template_key(st, TemplatePosition.Storage)] = st
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


class TemplateManager:
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
        self._templates: Dict[TemplateKey, Template] = dict()
        self._storage_compressed = bytes()

        self._refresh()

    def _refresh(self) -> None:
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

    def refresh(self) -> None:
        self._refresh()

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
    def templates(self) -> Dict[TemplateKey, Template]:
        return self._templates

    @property
    def storage_compressed(self) -> bytes:
        return self._storage_compressed

    def keys(self) -> KeysView[TemplateKey]:
        return self._templates.keys()

    def values(self) -> ValuesView[Template]:
        return self._templates.values()

    def decompress_templates(self, data: bytes) -> None:
        decompress_template_directory(self._template_directory, data)

    def find_template(self, category: str, name: str) -> Template:
        if category in self._storage_category_to_names.keys():
            position = TemplatePosition.Storage
            category_to_names = self._storage_category_to_names
        elif category in self._package_category_to_names.keys():
            position = TemplatePosition.Package
            category_to_names = self._package_category_to_names
        elif category in self._builtin_category_to_names.keys():
            position = TemplatePosition.Builtin
            category_to_names = self._builtin_category_to_names
        else:
            params_msg = f"{category}"
            raise ReccNotFoundError(f"Not found template category: {params_msg}")

        assert category in category_to_names
        if name not in category_to_names[category]:
            params_msg = f"category={category},name={name}"
            raise ReccNotFoundError(f"Not found template: {params_msg}")

        return self._templates[TemplateKey(position, category, name)]


class TemplateManagerMixin:

    _tm: TemplateManager

    def init_template_manager(self, root: str, venv_directory: str) -> None:
        self._tm = TemplateManager(root, venv_directory)

    def refresh_templates(self) -> None:
        assert self._tm is not None
        self._tm.refresh()

    def get_template_manager(self) -> TemplateManager:
        return self._tm

    def get_templates(self) -> Dict[TemplateKey, Template]:
        assert self._tm is not None
        return self._tm.templates

    def get_template_keys(self) -> KeysView[TemplateKey]:
        assert self._tm is not None
        return self._tm.keys()

    def get_template_values(self) -> ValuesView[Template]:
        assert self._tm is not None
        return self._tm.values()

    def compress_templates(self) -> bytes:
        assert self._tm is not None
        return self._tm.storage_compressed

    def decompress_templates(self, data: bytes) -> None:
        assert self._tm is not None
        self._tm.decompress_templates(data)
