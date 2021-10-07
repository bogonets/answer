# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.project import Project
from recc.variables.database import VISIBILITY_LEVEL_PRIVATE


class DbProject(metaclass=ABCMeta):
    """
    Database project interface.
    """

    @abstractmethod
    async def insert_project(
        self,
        group_uid: int,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility=VISIBILITY_LEVEL_PRIVATE,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_project_by_uid(
        self,
        uid: Optional[int] = None,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        visibility: Optional[int] = None,
        extra: Optional[Any] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_project_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_project_uid_by_group_uid_and_slug(
        self, group_uid: int, slug: str
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_project_by_uid(self, uid: int) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def select_projects_by_group_uid(self, group_uid: int) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    async def select_projects_by_below_visibility(
        self, visibility: int
    ) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    async def select_projects(self) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    async def select_projects_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_projects_by_user_uid(self, user_uid: int) -> List[Project]:
        raise NotImplementedError
