# -*- coding: utf-8 -*-

import os
from recc.exception.recc_error import (
    ReccNotFoundError,
    ReccNoWritableError,
)


def test_directory(directory: str) -> None:
    if not os.path.exists(directory):
        error_msg = f"The `{directory}` does not exist."
        raise ReccNotFoundError(error_msg)

    if not os.path.isdir(directory):
        error_msg = f"The `{directory}` can only be of directory type."
        raise ReccNotFoundError(error_msg)


def test_readable_directory(directory: str) -> None:
    test_directory(directory)

    if not os.access(directory, os.R_OK):
        error_msg = f"You need read access to the `{directory}` directory."
        raise ReccNoWritableError(error_msg)


def test_writable_directory(directory: str) -> None:
    test_directory(directory)

    if not os.access(directory, os.W_OK):
        error_msg = f"You need write access to the `{directory}` directory."
        raise ReccNoWritableError(error_msg)


def prepare_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.mkdir(directory)


def prepare_readable_directory(directory: str) -> None:
    prepare_directory(directory)
    test_readable_directory(directory)


def prepare_writable_directory(directory: str) -> None:
    prepare_directory(directory)
    test_writable_directory(directory)
