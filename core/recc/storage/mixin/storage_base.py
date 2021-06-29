# -*- coding: utf-8 -*-

import os
from typing import Optional, List, Union, Iterable
from tempfile import mkdtemp
from recc.file.directory import (
    prepare_readable_directory,
    prepare_writable_directory,
    test_writable_directory,
    test_readable_directory,
)
from recc.file.path_utils import HOME_DIR
from recc.file.permission import is_readable_dir, is_writable_dir
from recc.system.user import change_user
from recc.system.group import change_group

STORAGE_HOME_DIR = os.path.join(HOME_DIR, ".recc")
STORAGE_GLOBAL_DIR = "/var/recc"


def _is_dir(directory: str, read_only=False) -> bool:
    if read_only:
        return is_readable_dir(directory)
    else:
        return is_writable_dir(directory)


def _test_directory(directory: str, read_only=False) -> None:
    if read_only:
        test_readable_directory(directory)
    else:
        test_writable_directory(directory)


def _prepare_directory(directory: str, read_only=False) -> None:
    if read_only:
        prepare_readable_directory(directory)
    else:
        prepare_writable_directory(directory)


def _change_owner(
    path: str,
    user: Optional[Union[str, int]] = None,
    group: Optional[Union[str, int]] = None,
) -> None:
    if user is not None:
        change_user(path, user)
    if group is not None:
        change_group(path, group)


def find_available_storage(
    directories: Optional[Union[str, List[str]]] = None,
    read_only=False,
    validate=True,
) -> str:
    """
    :param directories:
        List of candidate directories.
    :param read_only:
        Read only flag.
    :param validate:
        Run validation.
    """

    candidates = []
    if directories:
        if isinstance(directories, str):
            candidates += [directories]
        elif isinstance(directories, list):
            candidates += directories
    candidates += [STORAGE_HOME_DIR, STORAGE_GLOBAL_DIR]

    for cursor in candidates:
        if cursor:
            if validate and not _is_dir(cursor, read_only):
                continue
            return cursor

    raise FileNotFoundError("Not found storage directory.")


class StorageBaseMixin:

    _root_dir: str
    _names: List[str]
    _read_only: bool

    def init_storage(
        self,
        root_dir: Optional[str] = None,
        subdir_names: Optional[Iterable[str]] = None,
        user: Optional[Union[str, int]] = None,
        group: Optional[Union[str, int]] = None,
        last_temp_candidate=True,
        read_only=False,
        validate=True,
        prepare=True,
    ) -> None:
        """
        :param root_dir:
            Root directory.
        :param subdir_names:
            List of candidate directories.
        :param user:
            User name or id.
        :param group:
            Group name or id.
        :param last_temp_candidate:
            If no storage is available, a temporary directory is used.
        :param read_only:
            Read only flag.
        :param validate:
            Run validation.
        :param prepare:
            Prepare subdirectories.
        """

        try:
            if root_dir:
                if validate:
                    _test_directory(root_dir, read_only)
                # Don't use `os.path.abspath` method.
                # When the core references the task's storage, the path is broken.
                candidate = root_dir
            else:
                candidate = find_available_storage(
                    read_only=read_only, validate=validate
                )
        except:  # noqa
            if not last_temp_candidate:
                raise
            candidate = mkdtemp(suffix="recc", prefix="storage")

        if validate:
            assert _is_dir(candidate, read_only)

        self._root_dir = candidate
        self._names = list(subdir_names) if subdir_names else list()
        self._read_only = read_only

        if prepare:
            _change_owner(self._root_dir, user, group)

            for name in self._names:
                subdir = os.path.join(self._root_dir, name)
                _prepare_directory(subdir, read_only)
                _change_owner(subdir, user, group)

    def get_root_directory(self) -> str:
        return self._root_dir

    def get_subdirectories(self) -> List[str]:
        """Returns the subdirectories of the workspace."""

        def _filter(name) -> bool:
            return os.path.isdir(os.path.join(self._root_dir, name))

        return list(filter(_filter, os.listdir(self._root_dir)))
