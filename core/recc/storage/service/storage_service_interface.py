# -*- coding: utf-8 -*-

from typing import Optional, List, Iterable, Dict, Tuple
from dataclasses import dataclass
from datetime import datetime
from abc import ABCMeta, abstractmethod


@dataclass
class StorageServiceObject:
    bucket: str
    name: str
    tag: str
    content_type: str
    size: int
    modified: datetime
    is_dir: bool
    owner_id: Optional[str] = None
    owner_name: Optional[str] = None
    version_id: Optional[str] = None


class StorageServiceInterface(metaclass=ABCMeta):
    """
    Cache Store interface.
    """

    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def make_bucket(self, bucket: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_buckets(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def exists_bucket(self, bucket: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def remove_bucket(self, bucket: str, force=False) -> None:
        raise NotImplementedError

    @abstractmethod
    async def expiration_bucket_by_tags(
        self,
        bucket: str,
        rule_id: Optional[str] = None,
        prefix: Optional[str] = None,
        tag_pair: Optional[Tuple[str, str]] = None,
        date: Optional[datetime] = None,
        days: Optional[int] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_object(self, bucket: str, name: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def put_object(
        self,
        bucket: str,
        name: str,
        content: bytes,
        content_type: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_object(self, bucket: str, prefix: str, recursive=False) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    async def remove_object(self, bucket: str, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_objects(self, bucket: str, names: Iterable[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_state(self, bucket: str, name: str) -> Optional[StorageServiceObject]:
        raise NotImplementedError

    @abstractmethod
    async def exists_object(self, bucket: str, name: str) -> bool:
        raise NotImplementedError
