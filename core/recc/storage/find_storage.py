# -*- coding: utf-8 -*-

import os
from tempfile import mkdtemp
from typing import List, Optional, Union

from recc.filesystem.path_utils import HOME_DIR
from recc.filesystem.permission import (
    is_readable_dir,
    is_writable_dir,
    prepare_readable_directory,
    prepare_writable_directory,
    test_readable_directory,
    test_writable_directory,
)
from recc.system.group import change_group
from recc.system.user import change_user
from recc.variables.storage import (
    DEFAULT_STORAGE_GLOBAL_DIR,
    DEFAULT_STORAGE_HOME_NAME,
    DEFAULT_TEMP_STORAGE_PREFIX,
    DEFAULT_TEMP_STORAGE_SUFFIX,
)


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
    candidates += [
        os.path.join(HOME_DIR, DEFAULT_STORAGE_HOME_NAME),
        DEFAULT_STORAGE_GLOBAL_DIR,
    ]

    for cursor in candidates:
        if cursor:
            if validate and not _is_dir(cursor, read_only):
                continue
            return cursor

    raise FileNotFoundError("Not found storage directory.")


def find_available_storage_or_temp_directory(
    last_temp_candidate=True,
    read_only=False,
    validate=True,
    *,
    temp_suffix=DEFAULT_TEMP_STORAGE_SUFFIX,
    temp_prefix=DEFAULT_TEMP_STORAGE_PREFIX,
) -> str:
    try:
        candidate = find_available_storage(read_only=read_only, validate=validate)
    except FileNotFoundError:
        if not last_temp_candidate:
            raise
        candidate = mkdtemp(suffix=temp_suffix, prefix=temp_prefix)

    if validate:
        assert _is_dir(candidate, read_only=read_only)

    return candidate


def directory_or_temp_directory(
    directory: str,
    last_temp_candidate=True,
    read_only=False,
    validate=True,
    *,
    temp_suffix=DEFAULT_TEMP_STORAGE_SUFFIX,
    temp_prefix=DEFAULT_TEMP_STORAGE_PREFIX,
) -> str:
    try:
        if validate:
            _test_directory(directory, read_only=read_only)
        # Don't use `os.path.abspath` method.
        # When the core references the task's storage, the path is broken.
        candidate = directory
    except:  # noqa
        if not last_temp_candidate:
            raise
        candidate = mkdtemp(suffix=temp_suffix, prefix=temp_prefix)

    if validate:
        assert _is_dir(candidate, read_only=read_only)

    return candidate
