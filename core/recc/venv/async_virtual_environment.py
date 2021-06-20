# -*- coding: utf-8 -*-

import sys
import os
from types import SimpleNamespace
from typing import Optional
from venv import EnvBuilder
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess


def _get_site_packages_dir(env_dir) -> str:
    if sys.platform == "win32":
        return os.path.join(env_dir, "Lib", "site-packages")
    else:
        return os.path.join(
            env_dir, "lib", "python%d.%d" % sys.version_info[:2], "site-packages"
        )


class AsyncVirtualEnvironment:
    def __init__(
        self,
        root_directory: str,
        system_site_packages=False,
        pip_timeout: Optional[float] = None,
    ):
        self._root_directory = root_directory
        self._pip_timeout = pip_timeout if pip_timeout else 0.0
        self._venv = EnvBuilder(
            system_site_packages=system_site_packages,
            clear=False,
            symlinks=False,
            upgrade=False,
            with_pip=True,
            prompt=None,
        )

        self._context = self._venv.ensure_directories(os.path.abspath(root_directory))
        if not hasattr(self._context, "pip_exe"):
            self._context.pip_exe = os.path.join(
                self._context.bin_path, "pip%d.%d" % sys.version_info[:2]
            )
        if not hasattr(self._context, "site_packages_dir"):
            self._context.site_packages_dir = _get_site_packages_dir(root_directory)

    @property
    def root(self) -> str:
        return self._root_directory

    @property
    def context(self) -> SimpleNamespace:
        return self._context

    @property
    def bin_name(self) -> str:
        return self.context.bin_name

    @property
    def bin_path(self) -> str:
        return self.context.bin_path

    @property
    def env_dir(self) -> str:
        return self.context.env_dir

    @property
    def env_exe(self) -> str:
        return self.context.env_exe

    @property
    def env_name(self) -> str:
        return self.context.env_name

    @property
    def executable(self) -> str:
        return self.context.executable

    @property
    def inc_path(self) -> str:
        return self.context.inc_path

    @property
    def prompt(self) -> str:
        return self.context.prompt

    @property
    def python_dir(self) -> str:
        return self.context.python_dir

    @property
    def python_exe(self) -> str:
        return self.context.python_exe

    @property
    def pip_exe(self) -> str:
        return self._context.pip_exe

    @property
    def site_packages_dir(self) -> str:
        return self._context.site_packages_dir

    def _create(self) -> None:
        self._venv.create(self._root_directory)

    def _create_if_not_exists(self) -> None:
        if not os.path.exists(self.env_exe):
            self._venv.create(self._root_directory)

    def _clear(self) -> None:
        self._venv.clear_directory(self._root_directory)

    def _create_configuration(self) -> None:
        self._venv.create_configuration(self._context)

    def _setup_python(self) -> None:
        self._venv.setup_python(self._context)

    def _setup_scripts(self) -> None:
        self._venv.setup_scripts(self._context)

    def _upgrade_dependencies(self) -> None:
        func = getattr(self._venv, "upgrade_dependencies")
        if func is None:
            raise NotImplementedError
        assert sys.version_info >= (3, 9)
        func(self._context)

    def _post_setup(self) -> None:
        self._venv.post_setup(self._context)

    def _install_scripts(self, path: str) -> None:
        self._venv.install_scripts(self._context, path)

    async def _setup_pip(self) -> None:
        await AsyncPythonSubprocess(self.env_exe).ensure_pip()

    async def create(self) -> None:
        # See issue 24875. We need system_site_packages to be False
        # until after pip is installed.
        true_system_site_packages = self._venv.system_site_packages
        self._venv.system_site_packages = False
        self._create_configuration()
        self._setup_python()
        if self._venv.with_pip:
            await self._setup_pip()
        if not self._venv.upgrade:
            self._setup_scripts()
            self._post_setup()
        if true_system_site_packages:
            # We had set it to False before, now
            # restore it and rewrite the configuration
            self._venv.system_site_packages = True
            self._create_configuration()

    async def create_if_not_exists(self) -> None:
        if not os.path.exists(self.env_exe):
            await self.create()

    def create_python_subprocess(self) -> AsyncPythonSubprocess:
        return AsyncPythonSubprocess(self.env_exe, self._pip_timeout)
