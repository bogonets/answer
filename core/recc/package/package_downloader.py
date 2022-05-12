# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
from hashlib import sha256, sha512
from typing import Iterable, Optional

from recc.logging.logging import recc_package_logger as logger
from recc.network.access import accessible_network


class HashMismatchError(ValueError):
    def __init__(
        self,
        filename: str,
        hash_method: str,
        expected_hash_value: str,
        actually_hash_value: str,
    ):
        self.filename = filename
        self.hash_method = hash_method
        self.expected_hash_value = expected_hash_value
        self.actually_hash_value = actually_hash_value

        msg0 = f"'Hash('{hash_method}') mismatch: '{filename}'"
        msg1 = f"\n  Expected: '{expected_hash_value}'"
        msg2 = f"\n  Actually: '{actually_hash_value}'"
        super().__init__(msg0 + msg1 + msg2)


@dataclass
class PackageInfo:
    filename: str
    hash_method: str
    expected_hash_value: str


class PackageDownloader:
    def __init__(self, download_dir: str, temp_dir: str, logging_encoding="utf-8"):
        self.download_dir = download_dir
        self.temp_dir = temp_dir
        self.logging_encoding = logging_encoding

    @staticmethod
    def test_accessible_pypi(timeout: Optional[float] = None) -> bool:
        return accessible_network("https://pypi.org/", timeout)

    @staticmethod
    def read_hash(path: str, method: str) -> str:
        with open(path, "rb") as f:
            content = f.read()

            if method == "sha256":
                return sha256(content).hexdigest()
            elif method == "sha512":
                return sha512(content).hexdigest()
            else:
                raise ValueError(f"Unsupported hash method: {method}")

    def _stdout_callback(self, data: bytes) -> None:
        line = str(data, encoding=self.logging_encoding).rstrip()
        if line:
            logger.debug(line)

    def _stderr_callback(self, data: bytes) -> None:
        line = str(data, encoding=self.logging_encoding).rstrip()
        if line:
            logger.warning(line)

    def validate_package(
        self,
        filename: str,
        hash_method: str,
        expected_hash_value: str,
    ) -> None:
        download_file = os.path.join(self.download_dir, filename)
        if not os.path.isfile(download_file):
            raise FileNotFoundError(f"Package file not found: {download_file}")

        actually_hash_value = self.read_hash(download_file, hash_method)
        if expected_hash_value != actually_hash_value:
            raise HashMismatchError(
                download_file,
                hash_method,
                expected_hash_value,
                actually_hash_value,
            )

    async def download_package(self, package: str) -> None:
        raise NotImplementedError

    async def download_packages(self, packages: Iterable[str]) -> None:
        for package in packages:
            await self.download_package(package)
