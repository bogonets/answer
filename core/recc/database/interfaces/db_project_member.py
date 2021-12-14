# -*- coding: utf-8 -*-

from typing import List
from abc import ABCMeta, abstractmethod
from recc.database.struct.project_member import ProjectMember


class DbProjectMember(metaclass=ABCMeta):
    """
    Database project member interface.
    """

    @abstractmethod
    async def insert_project_member(
        self, project_uid: int, user_uid: int, role_uid: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_member_role(
        self, project_uid: int, user_uid: int, role_uid: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_project_member(self, project_uid: int, user_uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_project_member(
        self, project_uid: int, user_uid: int
    ) -> ProjectMember:
        raise NotImplementedError

    @abstractmethod
    async def select_project_members_by_project_uid(
        self, project_uid: int
    ) -> List[ProjectMember]:
        raise NotImplementedError

    @abstractmethod
    async def select_project_members_by_user_uid(
        self, user_uid: int
    ) -> List[ProjectMember]:
        raise NotImplementedError

    @abstractmethod
    async def select_project_members(self) -> List[ProjectMember]:
        raise NotImplementedError
