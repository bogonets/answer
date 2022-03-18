# -*- coding: utf-8 -*-

import os
import sys
import site
from abc import abstractmethod
from typing import List, Optional
from overrides import overrides

real_prefix = "real_prefix"

X = sys.version_info[0]
Y = sys.version_info[1]
XY = f"{X}{Y}"
X_Y = f"{X}.{Y}"

LIB_PYTHON_ZIP = f"{sys.base_prefix}/{sys.platlibdir}/python{XY}.zip"
LIB_PYTHON = f"{sys.base_prefix}/{sys.platlibdir}/python{X_Y}"
LIB_PYTHON_LIB_DYNLOAD = f"{sys.base_prefix}/{sys.platlibdir}/python{X_Y}/lib-dynload"

PATH = "PATH"
VIRTUAL_ENV = "VIRTUAL_ENV"


class ContextChanger:
    @abstractmethod
    def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    def __enter__(self):
        self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def __aenter__(self):
        raise RuntimeError(
            "Accessing the sys package while the event loop is running causes problems"
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise RuntimeError(
            "Accessing the sys package while the event loop is running causes problems"
        )


class FakeContextChanger(ContextChanger):
    @overrides
    def open(self) -> None:
        pass

    @overrides
    def close(self) -> None:
        pass


class VenvContextChanger(ContextChanger):
    """
    References:
        - https://docs.python.org/3/library/sys.html
        - https://docs.python.org/3/library/venv.html
        - https://peps.python.org/pep-0405/
    """

    _sys_prefix: str
    _sys_exec_prefix: str
    _sys_executable: str
    _sys_path: List[str]
    _sys_real_prefix: Optional[str]
    _env_path: Optional[str]
    _env_virtual_env: Optional[str]

    def __init__(
        self,
        env_dir: str,
        env_exe: str,
        bin_path: str,
        site_packages_dir: str,
    ):
        self.env_dir = env_dir
        self.env_exe = env_exe
        self.bin_path = bin_path
        self.site_packages_dir = site_packages_dir

    @overrides
    def open(self) -> None:
        self._sys_prefix = sys.prefix
        self._sys_exec_prefix = sys.exec_prefix
        self._sys_executable = sys.executable
        self._sys_path = sys.path

        sys.prefix = self.env_dir
        sys.exec_prefix = self.env_dir
        sys.executable = self.env_exe
        sys.path = [
            LIB_PYTHON_ZIP,
            LIB_PYTHON,
            LIB_PYTHON_LIB_DYNLOAD,
        ]
        site.addsitedir(self.site_packages_dir)

        self._sys_real_prefix = getattr(sys, real_prefix, None)
        setattr(sys, real_prefix, self.env_dir)

        self._env_path = os.environ.get(PATH, None)
        self._env_virtual_env = os.environ.get(VIRTUAL_ENV, None)

        os.environ[PATH] = os.pathsep.join(
            [self.bin_path] + os.environ.get(PATH, "").split(os.pathsep)
        )
        os.environ[VIRTUAL_ENV] = self.env_dir

    @staticmethod
    def _restore_env(key: str, original: Optional[str]):
        if original is not None:
            os.environ[key] = original
        else:
            os.environ.pop(key)

    @overrides
    def close(self) -> None:
        sys.prefix = self._sys_prefix
        sys.exec_prefix = self._sys_exec_prefix
        sys.executable = self._sys_executable
        sys.path = self._sys_path

        assert hasattr(sys, real_prefix)
        if self._sys_real_prefix is not None:
            setattr(sys, real_prefix, self._sys_real_prefix)
        else:
            delattr(sys, real_prefix)

        self._restore_env(PATH, self._env_path)
        self._restore_env(VIRTUAL_ENV, self._env_virtual_env)
