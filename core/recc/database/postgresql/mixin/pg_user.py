# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.chrono.datetime import today
from recc.database.struct.user import User, PassInfo
from recc.database.interfaces.db_user import DbUser
from recc.database.postgresql.mixin._pg_base import PgBase
from recc.database.postgresql.query.user import (
    INSERT_USER,
    UPDATE_USER_LAST_LOGIN_BY_UID,
    UPDATE_USER_PASSWORD_AND_SALT_BY_UID,
    UPDATE_USER_EXTRA_BY_UID,
    DELETE_USER_BY_UID,
    SELECT_USER_USERNAME_BY_UID,
    SELECT_USER_UID_BY_USERNAME,
    SELECT_USER_EXISTS_BY_USERNAME,
    SELECT_USER_PASSWORD_AND_SALT_BY_UID,
    SELECT_USER_EXTRA_BY_UID,
    SELECT_USER_BY_UID,
    SELECT_USER_ALL,
    SELECT_USER_USERNAME,
    SELECT_USER_ADMIN_COUNT,
    SELECT_USER_COUNT,
    get_update_user_query_by_uid,
)


class PgUser(DbUser, PgBase):
    @staticmethod
    def signup_normalize_text(text: Optional[str]) -> Optional[str]:
        if text is None:
            return None
        text = text.strip()
        return text if text else None

    @overrides
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
        created = created_at if created_at else today()
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

    @overrides
    async def update_user_last_login_by_uid(
        self,
        uid: int,
        last_login: Optional[datetime] = None,
    ) -> None:
        login = last_login if last_login else today()
        await self.execute(UPDATE_USER_LAST_LOGIN_BY_UID, uid, login)

    @overrides
    async def update_user_password_and_salt_by_uid(
        self,
        uid: int,
        password: str,
        salt: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(
            UPDATE_USER_PASSWORD_AND_SALT_BY_UID,
            uid,
            password,
            salt,
            updated,
        )

    @overrides
    async def update_user_extra_by_uid(
        self,
        uid: int,
        extra: Any,
        updated_at: Optional[datetime] = None,
    ) -> None:
        updated = updated_at if updated_at else today()
        await self.execute(UPDATE_USER_EXTRA_BY_UID, uid, extra, updated)

    @overrides
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
        updated = updated_at if updated_at else today()
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

    @overrides
    async def delete_user_by_uid(self, uid: int) -> None:
        await self.execute(DELETE_USER_BY_UID, uid)

    @overrides
    async def select_user_username_by_uid(self, uid: int) -> str:
        return await self.column(str, SELECT_USER_USERNAME_BY_UID, uid)

    @overrides
    async def select_user_uid_by_username(self, username: str) -> int:
        return await self.column(int, SELECT_USER_UID_BY_USERNAME, username)

    @overrides
    async def select_user_exists_by_username(self, username: str) -> bool:
        return await self.column(bool, SELECT_USER_EXISTS_BY_USERNAME, username)

    @overrides
    async def select_user_password_and_salt_by_uid(self, uid: int) -> PassInfo:
        return await self.row(PassInfo, SELECT_USER_PASSWORD_AND_SALT_BY_UID, uid)

    @overrides
    async def select_user_extra_by_uid(self, uid: int) -> Any:
        return await self.fetch_first_row_column(SELECT_USER_EXTRA_BY_UID, uid)

    @overrides
    async def select_user_by_uid(self, uid: int) -> User:
        return await self.row(User, SELECT_USER_BY_UID, uid)

    @overrides
    async def select_users(self) -> List[User]:
        return await self.rows(User, SELECT_USER_ALL)

    @overrides
    async def select_users_count(self) -> int:
        return await self.column(int, SELECT_USER_COUNT)

    @overrides
    async def select_admin_count(self) -> int:
        return await self.column(int, SELECT_USER_ADMIN_COUNT)

    @overrides
    async def select_exists_admin_user(self) -> bool:
        return await self.select_admin_count() >= 1

    @overrides
    async def select_user_username(self) -> List[str]:
        rows = await self.fetch_rows(SELECT_USER_USERNAME)
        return [row["username"] for row in rows]
