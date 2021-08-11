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
    async def create_user(
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
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_last_login_by_username(
        self, username: str, last_login=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_password_and_salt_by_uid(
        self, uid: int, password: str, salt: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_password_and_salt_by_username(
        self, username: str, password: str, salt: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_extra_by_username(
        self, username: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_by_username(
        self,
        username: str,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin: Optional[bool] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_name(self, username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_uid_by_username(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exist_user(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_user_password_and_salt(self, username: str) -> PassInfo:
        raise NotImplementedError

    @abstractmethod
    async def get_user_extra(self, username: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_users(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_users_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_admin_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exists_admin_user(self) -> bool:
        raise NotImplementedError
