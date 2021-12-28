# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase
from recc.storage.service.minio.minio_storage_service import MinioStorageService
from recc.argparse.default_parser import parse_arguments_to_core_config


class MinioTestCase(IsolatedAsyncioTestCase):
    async def _setup(self):
        self.config = parse_arguments_to_core_config()
        self.host = self.config.storage_host
        self.port = self.config.storage_port
        self.user = self.config.storage_user
        self.pw = self.config.storage_pw
        self.region = self.config.storage_region
        self.secure = self.config.storage_secure
        self.bucket = "recc.test"

        self.minio = MinioStorageService(
            ss_host=self.host,
            ss_port=self.port,
            ss_user=self.user,
            ss_pw=self.pw,
            ss_region=self.region,
            ss_secure=self.secure,
        )

        await self.minio.open()
        self.assertTrue(self.minio.is_open())

        if await self.minio.exists_bucket(self.bucket):
            await self.minio.remove_bucket(self.bucket, force=True)

    async def asyncSetUp(self):
        try:
            await self._setup()
        except BaseException as e:  # noqa
            print(e)
            await self._teardown()
            raise

    async def _teardown(self):
        if await self.minio.exists_bucket(self.bucket):
            await self.minio.remove_bucket(self.bucket, force=True)
        await self.minio.close()
        self.assertFalse(self.minio.is_open())

    async def asyncTearDown(self):
        await self._teardown()
