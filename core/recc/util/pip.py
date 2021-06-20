# -*- coding: utf-8 -*-

import os
from typing import Optional, List, Tuple


def _install_package(name: str, version: Optional[str] = None) -> None:
    install_command = f"pip install {name}"
    if version:
        install_command += f"=={version}"

    print(f"Install {name} ...")
    code = os.system(install_command)
    if code == 0:
        print(f"{name} installation was successful.")
    else:
        print(f"{name} installation failed(code={code})")


def _test_and_install_module(import_path: str, package_name: str, version: str) -> None:
    try:
        __import__(import_path)
    except ImportError:  # noqa
        _install_package(package_name, version)


def _test_and_install_modules(modules: List[Tuple[str, str, str]]) -> None:
    for package_name, import_path, version in modules:
        _test_and_install_module(package_name, import_path, version)
