# -*- coding: utf-8 -*-

from typing import Any, Optional, List, Dict
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.task import Task


class DbTask(metaclass=ABCMeta):
    """
    Database task interface.
    """

    @abstractmethod
    async def insert_task(
        self,
        project_uid: int,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        rpc_address: Optional[str] = None,
        auth_algorithm: Optional[str] = None,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_task_description_by_uid(
        self,
        uid: int,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_description_by_slug(
        self,
        project_uid: int,
        slug: str,
        description: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_extra_by_slug(
        self,
        project_uid: int,
        slug: str,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_keys_by_uid(
        self,
        uid: int,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_keys_by_slug(
        self,
        project_uid: int,
        slug: str,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_by_uid(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        rpc_address: Optional[str] = None,
        auth_algorithm: Optional[str] = None,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_task_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_task_by_slug(self, project_uid: int, slug: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_task_by_uid(self, uid: int) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def select_task_by_slug(self, project_uid: int, slug: str) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def select_task_uid_by_slug(self, project_uid: int, slug: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_task_by_project_uid(self, project_uid: int) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    async def select_task_by_fullpath(
        self, group_slug: str, project_slug: str, task_slug: str
    ) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def select_task_uid_by_fullpath(
        self, group_slug: str, project_slug: str, task_slug: str
    ) -> int:
        raise NotImplementedError
