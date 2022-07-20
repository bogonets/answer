# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any, List, Optional

from recc.chrono.datetime import tznow
from recc.database.mixin._pg_base import PgBase
from recc.database.query.user import (
    DELETE_USER_BY_UID,
    INSERT_USER,
    SELECT_USER_ADMIN_COUNT,
    SELECT_USER_ALL,
    SELECT_USER_BY_UID,
    SELECT_USER_COUNT,
    SELECT_USER_EXISTS_BY_USERNAME,
    SELECT_USER_EXTRA_BY_UID,
    SELECT_USER_PASSWORD_AND_SALT_BY_UID,
    SELECT_USER_UID_BY_USERNAME,
    SELECT_USER_USERNAME,
    SELECT_USER_USERNAME_BY_UID,
    UPDATE_USER_EXTRA_BY_UID,
    UPDATE_USER_LAST_LOGIN_BY_UID,
    UPDATE_USER_PASSWORD_AND_SALT_BY_UID,
    get_update_user_query_by_uid,
)
from recc.packet.user import PassInfo, User


class PgUser(PgBase):
    @staticmethod
    def signup_normalize_text(text: Optional[str]) -> Optional[str]:
        if text is None:
            return None
        text = text.strip()
        return text if text else None

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
        created = created_at if created_at else tznow()
        return await self.column(
            int,
            INSERT_USER,
            username,
            password,
            salt,
            self.signup_normalize_text(nickname),
            self.signup_normalize_text(email),
            self.signup_normalize_text(phone1),
            self.signup_normalize_text(phone2),
            is_admin,
            extra,
            created,
        )

    async def update_user_last_login_by_uid(
        self,
        uid: int,
        last_login: Optional[datetime] = None,
    ) -> None:
        login = last_login if last_login else tznow()
        await self.execute(UPDATE_USER_LAST_LOGIN_BY_UID, uid, login)

    async def update_user_password_and_salt_by_uid(
        self,
        uid: int,
        password: str,
        salt: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(
            UPDATE_USER_PASSWORD_AND_SALT_BY_UID,
            uid,
            password,
            salt,
            updated,
        )

    async def update_user_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else tznow()
        await self.execute(UPDATE_USER_EXTRA_BY_UID, uid, extra, updated)

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
        updated = updated_at if updated_at else tznow()
        query, args = get_update_user_query_by_uid(
            uid=uid,
            username=username,
            nickname=nickname,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=is_admin,
            extra=extra,
            updated_at=updated,
        )
        await self.execute(query, *args)

    async def delete_user_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_USER_BY_UID, uid)

    async def select_user_username_by_uid(self, uid: int) -> str:
        return await self.column(str, SELECT_USER_USERNAME_BY_UID, uid)

    async def select_user_uid_by_username(self, username: str) -> int:
        return await self.column(int, SELECT_USER_UID_BY_USERNAME, username)

    async def select_user_exists_by_username(self, username: str) -> bool:
        return await self.column(bool, SELECT_USER_EXISTS_BY_USERNAME, username)

    async def select_user_password_and_salt_by_uid(self, uid: int) -> PassInfo:
        return await self.row(PassInfo, SELECT_USER_PASSWORD_AND_SALT_BY_UID, uid)

    async def select_user_extra_by_uid(self, uid: int) -> Any:
        return await self.fetch_first_row_column(SELECT_USER_EXTRA_BY_UID, uid)

    async def select_user_by_uid(self, uid: int) -> User:
        return await self.row(User, SELECT_USER_BY_UID, uid)

    async def select_users(self) -> List[User]:
        return await self.rows(User, SELECT_USER_ALL)

    async def select_users_count(self) -> int:
        return await self.column(int, SELECT_USER_COUNT)

    async def select_admin_count(self) -> int:
        return await self.column(int, SELECT_USER_ADMIN_COUNT)

    async def select_exists_admin_user(self) -> bool:
        return await self.select_admin_count() >= 1

    async def select_user_username(self) -> List[str]:
        rows = await self.fetch_rows(SELECT_USER_USERNAME)
        return [row["username"] for row in rows]
