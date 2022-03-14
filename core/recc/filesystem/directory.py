# -*- coding: utf-8 -*-

import os


def test_directory(directory: str) -> None:
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The `{directory}` does not exist")

    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The `{directory}` can only be of directory type")


def test_readable_directory(directory: str) -> None:
    test_directory(directory)

    if not os.access(directory, os.R_OK):
        raise PermissionError(f"You need read access to the `{directory}` directory")


def test_writable_directory(directory: str) -> None:
    test_directory(directory)

    if not os.access(directory, os.W_OK):
        raise PermissionError(f"You need write access to the `{directory}` directory")


def prepare_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.mkdir(directory)


def prepare_readable_directory(directory: str) -> None:
    prepare_directory(directory)
    test_readable_directory(directory)


def prepare_writable_directory(directory: str) -> None:
    prepare_directory(directory)
    test_writable_directory(directory)
