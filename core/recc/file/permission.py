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
