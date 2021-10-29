# -*- coding: utf-8 -*-

from typing import Optional, List, Iterable
from overrides import overrides
from io import BytesIO
from urllib3.response import HTTPResponse
from minio import Minio, S3Error
from minio.deleteobjects import DeleteObject
from recc.mime.mime_type import APPLICATION_OCTET_STREAM
from recc.storage.service.storage_service_interface import (
    StorageServiceObject,
    StorageServiceInterface,
)


class MinioStorageService(StorageServiceInterface):
    """
    Minio Storage Service.
    """

    def __init__(
        self,
        ss_host: str,
        ss_port: Optional[int] = None,
        ss_user: Optional[str] = None,
        ss_pw: Optional[str] = None,
        ss_region: Optional[str] = None,
        ss_secure=False,
        **kwargs,
    ):
        self._ss_host = ss_host
        self._ss_port = ss_port
        self._ss_user = ss_user
        self._ss_pw = ss_pw
        self._ss_region = ss_region
        self._ss_secure = ss_secure
        self._kwargs = kwargs
        self._minio: Optional[Minio] = None

    @property
    def address(self) -> str:
        if self._ss_port is not None:
            return f"{self._ss_host}:{self._ss_port}"
        else:
            return self._ss_host

    @overrides
    def is_open(self) -> bool:
        return self._minio is not None

    @overrides
    async def open(self) -> None:
        self._minio = Minio(
            self.address,
            access_key=self._ss_user,
            secret_key=self._ss_pw,
            region=self._ss_region,
            secure=self._ss_secure,
        )

    @overrides
    async def close(self) -> None:
        self._minio = None

    @property
    def minio(self) -> Minio:
        assert self._minio is not None
        return self._minio

    @overrides
    async def make_bucket(self, bucket: str) -> None:
        self.minio.make_bucket(bucket)

    @overrides
    async def list_buckets(self) -> List[str]:
        return [bucket.name for bucket in self.minio.list_buckets()]

    @overrides
    async def exists_bucket(self, bucket: str) -> bool:
        return self.minio.bucket_exists(bucket)

    @overrides
    async def remove_bucket(self, bucket: str, force=False) -> None:
        if force:
            objects = self.minio.list_objects(bucket, recursive=True)
            delete_objects = [DeleteObject(o.object_name) for o in objects]
            errors = self.minio.remove_objects(bucket, delete_objects)
            for error in errors:  # Important !!
                raise RuntimeError(str(error))
        self.minio.remove_bucket(bucket)

    @overrides
    async def get_object(self, bucket: str, name: str) -> bytes:
        response: Optional[HTTPResponse] = None
        try:
            response = self.minio.get_object(bucket, name)
            return response.read()
        finally:
            if response:
                response.close()
                response.release_conn()

    @overrides
    async def put_object(
        self,
        bucket: str,
        name: str,
        content: bytes,
        content_type: Optional[str] = None,
    ) -> None:
        self.minio.put_object(
            bucket,
            name,
            BytesIO(content),
            len(content),
            content_type if content_type else APPLICATION_OCTET_STREAM,
        )

    @overrides
    async def list_object(
        self,
        bucket: str,
        prefix: Optional[str] = None,
        recursive=False,
    ) -> List[str]:
        objects = self.minio.list_objects(bucket, prefix, recursive)
        return [o.object_name for o in objects]

    @overrides
    async def remove_object(self, bucket: str, name: str) -> None:
        self.minio.remove_object(bucket, name)

    @overrides
    async def remove_objects(self, bucket: str, names: Iterable[str]) -> None:
        delete_objects = [DeleteObject(n) for n in names]
        errors = self.minio.remove_objects(bucket, delete_objects)
        for error in errors:  # Important !!
            raise RuntimeError(str(error))

    @overrides
    async def get_state(self, bucket: str, name: str) -> Optional[StorageServiceObject]:
        try:
            stat = self.minio.stat_object(bucket, name)
            return StorageServiceObject(
                bucket=stat.bucket_name,
                name=stat.object_name,
                tag=stat.etag,
                content_type=stat.content_type,
                size=stat.size,
                modified=stat.last_modified,
                is_dir=stat.is_dir,
                owner_id=stat.owner_id,
                owner_name=stat.owner_name,
                version_id=stat.version_id,
            )
        except S3Error as e:
            if e.code == "NoSuchKey":
                return None
            else:
                raise

    @overrides
    async def exists_object(self, bucket: str, name: str) -> bool:
        try:
            self.minio.stat_object(bucket, name)
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            else:
                raise
        else:
            return True