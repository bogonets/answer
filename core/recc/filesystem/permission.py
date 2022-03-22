# -*- coding: utf-8 -*-

import os
import stat


def change_readable(path: str):
    os.chmod(path, stat.S_IRUSR)


def change_writable(path: str):
    os.chmod(path, stat.S_IWUSR)


def change_executable(path: str):
    os.chmod(path, stat.S_IXUSR)


def exists(path: str) -> bool:
    return os.path.exists(path)


def remove_file(path: str):
    os.unlink(path)


def remove_dir(path: str):
    os.rmdir(path)


def is_readable_file(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    if not os.access(path, os.R_OK):
        return False
    return True


def is_writable_file(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    if not os.access(path, os.W_OK):
        return False
    return True


def is_executable_file(path: str) -> bool:
    if not os.path.isfile(path):
        return False
    if not os.access(path, os.X_OK):
        return False
    return True


def is_readable_dir(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    if not os.access(path, os.R_OK):
        return False
    return True


def is_writable_dir(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    if not os.access(path, os.W_OK):
        return False
    return True


def is_executable_dir(path: str) -> bool:
    if not os.path.isdir(path):
        return False
    if not os.access(path, os.X_OK):
        return False
    return True


def test_directory(path: str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"The `{path}` does not exist")

    if not os.path.isdir(path):
        raise FileNotFoundError(f"The `{path}` can only be of path type")


def test_file(path: str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"The `{path}` does not exist")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"The `{path}` can only be of file type")


def test_readable_directory(path: str) -> None:
    test_directory(path)

    if not os.access(path, os.R_OK):
        raise PermissionError(f"You need read access to the `{path}` directory")


def test_writable_directory(path: str) -> None:
    test_directory(path)

    if not os.access(path, os.W_OK):
        raise PermissionError(f"You need write access to the `{path}` directory")


def test_readable_file(path: str) -> None:
    test_file(path)

    if not os.access(path, os.R_OK):
        raise PermissionError(f"You need read access to the `{path}` file")


def test_writable_file(path: str) -> None:
    test_file(path)

    if not os.access(path, os.W_OK):
        raise PermissionError(f"You need write access to the `{path}` file")


def prepare_directory(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def prepare_readable_directory(path: str) -> None:
    prepare_directory(path)
    test_readable_directory(path)


def prepare_writable_directory(path: str) -> None:
    prepare_directory(path)
    test_writable_directory(path)
