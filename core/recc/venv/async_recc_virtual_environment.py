# -*- coding: utf-8 -*-

import os
from typing import Optional, List
from overrides import overrides
from recc.venv.async_virtual_environment import AsyncVirtualEnvironment
from recc.package.recc_package import extract_recc_module
from recc.package.requirements_utils import RECC_REQUIREMENTS_MAIN
from recc.filesystem.directory import test_directory
from recc.variables.venv import DEFAULT_VENV_RECC_LOCAL_DIR_NAME


class AsyncReccVirtualEnvironment(AsyncVirtualEnvironment):
    def __init__(
        self,
        root_directory: str,
        system_site_packages=False,
        pip_timeout: Optional[float] = None,
        recc_dir_name=DEFAULT_VENV_RECC_LOCAL_DIR_NAME,
        pip_download_dir: Optional[str] = None,
    ):
        super().__init__(root_directory, system_site_packages, pip_timeout)
        self._recc_dir_name = recc_dir_name
        self._recc_dir = os.path.join(self.site_packages_dir, self._recc_dir_name)
        self._recc_pth_path = os.path.join(self.site_packages_dir, "recc.pth")
        self._pip_download_dir = pip_download_dir

    @property
    def recc_dir_name(self) -> str:
        return self._recc_dir_name

    @property
    def recc_dir(self) -> str:
        return self._recc_dir

    @property
    def recc_pth_path(self) -> str:
        return self._recc_pth_path

    @overrides
    async def create(self) -> None:
        await super().create()

        if not os.path.isdir(self.recc_dir):
            os.mkdir(self.recc_dir)
            extract_recc_module(self.recc_dir)
            with open(self._recc_pth_path, "w") as f:
                f.write(self.recc_dir_name)

            python = self.create_python_subprocess()

            if self._pip_download_dir:
                test_directory(self._pip_download_dir)
                install_subcommands = self.get_install_requirements_subcommands(
                    self._pip_download_dir
                )

                try:
                    # Check if you can install without a network connection.
                    # That is, a file that has already been downloaded may exist.
                    await python.start_pip_simply(*install_subcommands)
                except RuntimeError:
                    pass
                else:
                    return

                # If no files have been downloaded, they will be downloaded first.
                download_subcommands = self.get_download_requirements_subcommands(
                    self._pip_download_dir
                )
                await python.start_pip_simply(*download_subcommands)

                # Then, install from the downloaded file.
                await python.start_pip_simply(*install_subcommands)
            else:
                install_subcommands = self.get_install_requirements_subcommands()
                await python.start_pip_simply(*install_subcommands)

    @staticmethod
    def get_install_requirements_subcommands(
        pip_download_dir: Optional[str] = None,
    ) -> List[str]:
        subcommands = ["install", "--progress-bar=ascii"]
        if pip_download_dir:
            subcommands += ["--no-index", "--find-links", pip_download_dir]
        return subcommands + RECC_REQUIREMENTS_MAIN

    @staticmethod
    def get_download_requirements_subcommands(pip_download_dir: str) -> List[str]:
        return ["download", "--dest", pip_download_dir] + RECC_REQUIREMENTS_MAIN
