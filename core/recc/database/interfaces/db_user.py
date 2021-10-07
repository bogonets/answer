# -*- coding: utf-8 -*-

from typing import Any, Optional, List
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.database.struct.user import User, PassInfo


class DbUser(metaclass=ABCMeta):
    """
    Database user interface.
    """

    @abstractmethod
    async def insert_user(
        self,
        username: str,
        password: str,
        salt: str,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin=False,
        extra: Optional[Any] = None,
        created_at: Optional[datetime] = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_user_last_login_by_uid(
        self,
        uid: int,
        last_login: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_password_and_salt_by_uid(
        self,
        uid: int,
        password: str,
        salt: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_by_uid(
        self,
        uid: int,
        username: Optional[str] = None,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin: Optional[bool] = None,
        extra: Optional[Any] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def select_user_username_by_uid(self, uid: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def select_user_uid_by_username(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_user_exists_by_username(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def select_user_password_and_salt_by_uid(self, uid: int) -> PassInfo:
        raise NotImplementedError

    @abstractmethod
    async def select_user_extra_by_uid(self, uid: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def select_user_by_uid(self, uid: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def select_users(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def select_users_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_admin_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def select_exists_admin_user(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def select_user_username(self) -> List[str]:
        raise NotImplementedError
