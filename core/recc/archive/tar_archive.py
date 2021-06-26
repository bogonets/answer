# -*- coding: utf-8 -*-

import os
from tarfile import open as tar_open
from tarfile import TarFile, TarInfo, REGTYPE, DIRTYPE
from typing import Optional
from io import BytesIO


def compress_tar(
    path: str,
    mode="w",
    archive_name: Optional[str] = None,
    recursive=True,
) -> bytes:
    file_object = BytesIO()
    with tar_open(fileobj=file_object, mode=mode) as tar:
        tar.add(path, archive_name, recursive)
    return file_object.getvalue()


def compress_bytes(name: str, data: bytes, mode="w") -> bytes:
    file_object = BytesIO()
    with tar_open(fileobj=file_object, mode=mode) as tar:
        info = TarInfo(name=name)
        info.size = len(data)
        tar.addfile(info, BytesIO(data))
    return file_object.getvalue()


def remove_first_slash(path: str) -> str:
    return path[1:] if path.startswith("/") else path


def insert_last_slash(path: str) -> str:
    return path if path.endswith("/") else path + "/"


def file_info(path: str, size: int = 0, mode: int = 0o644) -> TarInfo:
    info = TarInfo(remove_first_slash(path))
    info.type = REGTYPE
    info.size = size
    info.mode = mode
    return info


def dir_info(path: str, mode: int = 0o644) -> TarInfo:
    info = TarInfo(insert_last_slash(remove_first_slash(path)))
    info.type = DIRTYPE
    info.mode = mode
    return info


def add_dirs(tar: TarFile, path: str, mode: int = 0o644) -> None:
    parent_dir = ""
    for directory in os.path.split(os.path.normpath(path)):
        if parent_dir:
            parent_dir = os.path.join(parent_dir, directory)
        else:
            parent_dir = directory
        if parent_dir:
            tar.addfile(dir_info(parent_dir, mode))
