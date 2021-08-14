# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.project import Project


class DbProject(metaclass=ABCMeta):
    """
    Database project interface.
    """

    @abstractmethod
    async def create_project(
        self,
        group_uid: int,
        name: str,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_description_by_name(
        self, group_uid: int, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_extra_by_name(
        self, group_uid: int, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_features_by_uid(
        self, uid: int, features: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_features_by_name(
        self,
        group_uid: int,
        name: str,
        features: List[str],
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_by_uid(
        self,
        uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_project_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_project_by_name(self, group_uid: int, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_uid(self, uid: int) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_name(self, group_uid: int, name: str) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_group_uid(self, group_uid: int) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_fullpath(
        self, group_slug: str, project_name: str
    ) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def get_project_uid_by_fullpath(
        self, group_slug: str, project_name: str
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_projects_count(self) -> int:
        raise NotImplementedError
