# -*- coding: utf-8 -*-

from typing import Optional
from recc.storage.service.storage_service_interface import StorageServiceInterface
from recc.storage.service.minio.minio_storage_service import MinioStorageService
from recc.variables.storage import STORAGE_SERVICE_TYPE_MINIO


def create_storage_service(
    ss_type: str,
    ss_host: str,
    ss_port: Optional[int] = None,
    ss_user: Optional[str] = None,
    ss_pw: Optional[str] = None,
    ss_region: Optional[str] = None,
    ss_secure=False,
    **kwargs,
) -> StorageServiceInterface:
    if ss_type == STORAGE_SERVICE_TYPE_MINIO:
        return MinioStorageService(
            ss_host, ss_port, ss_user, ss_pw, ss_region, ss_secure, **kwargs
        )
    else:
        raise ValueError(f"Unknown storage-service type: {ss_type}")
