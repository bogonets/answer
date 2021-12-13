# -*- coding: utf-8 -*-

from typing import List
from abc import ABCMeta, abstractmethod
from recc.database.struct.group_member import GroupMember
from recc.database.struct.group_join_member import (
    GroupJoinGroupMember,
    ProjectJoinGroupMember,
)


class DbGroupMember(metaclass=ABCMeta):
    """
    Database group member interface.
    """

    @abstractmethod
    async def insert_group_member(
        self, group_uid: int, user_uid: int, role_uid: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_member_role(
        self, group_uid: int, user_uid: int, role_uid: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_member(self, group_uid: int, user_uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_group_member(self, group_uid: int, user_uid: int) -> GroupMember:
        raise NotImplementedError

    @abstractmethod
    async def select_group_members_by_group_uid(
        self, group_uid: int
    ) -> List[GroupMember]:
        raise NotImplementedError

    @abstractmethod
    async def select_group_members_by_user_uid(
        self, user_uid: int
    ) -> List[GroupMember]:
        raise NotImplementedError

    @abstractmethod
    async def select_group_members(self) -> List[GroupMember]:
        raise NotImplementedError

    @abstractmethod
    async def select_group_members_join_group_by_user_uid(
        self, user_uid: int
    ) -> List[GroupJoinGroupMember]:
        raise NotImplementedError

    @abstractmethod
    async def select_group_member_join_group_by_user_uid_and_group_uid(
        self, user_uid: int, group_uid: int
    ) -> GroupJoinGroupMember:
        raise NotImplementedError

    @abstractmethod
    async def select_group_members_join_project_by_user_uid(
        self, user_uid: int
    ) -> List[ProjectJoinGroupMember]:
        raise NotImplementedError
