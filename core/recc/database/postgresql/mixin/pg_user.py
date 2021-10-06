# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from overrides import overrides
from recc.log.logging import recc_database_logger as logger
from recc.database.struct.user import User, PassInfo
from recc.database.interfaces.db_user import DbUser
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.query.user import (
    INSERT_USER,
    UPDATE_USER_LAST_LOGIN_BY_UID,
    UPDATE_USER_PASSWORD_AND_SALT_BY_UID,
    UPDATE_USER_EXTRA_BY_UID,
    SAFE_DELETE_USER_BY_UID,
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
        created_at=datetime.utcnow().astimezone(),
    ) -> int:
        query = INSERT_USER
        uit = await self.fetch_val(
            query,
            username,
            password,
            salt,
            self.signup_normalize_text(nickname),
            self.signup_normalize_text(email),
            self.signup_normalize_text(phone1),
            self.signup_normalize_text(phone2),
            is_admin,
            extra,
            created_at,
        )
        params_msg = f"username={username}"
        if is_admin:
            params_msg += ",admin"
        logger.info(f"insert_user({params_msg}) -> {uit}")
        return uit

    @overrides
    async def update_user_last_login_by_uid(
        self, uid: int, last_login=datetime.utcnow().astimezone()
    ) -> None:
        query = UPDATE_USER_LAST_LOGIN_BY_UID
        await self.execute(query, uid, last_login)
        params_msg = f"uid={uid},last_login={last_login}"
        logger.info(f"update_user_last_login_by_uid({params_msg}) ok.")

    @overrides
    async def update_user_password_and_salt_by_uid(
        self,
        uid: int,
        password: str,
        salt: str,
        updated_at=datetime.utcnow().astimezone(),
    ) -> None:
        query = UPDATE_USER_PASSWORD_AND_SALT_BY_UID
        await self.execute(query, uid, password, salt, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_user_password_and_salt_by_uid({params_msg}) ok.")

    @overrides
    async def update_user_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow().astimezone()
    ) -> None:
        query = UPDATE_USER_EXTRA_BY_UID
        await self.execute(query, uid, extra, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_user_extra_by_uid({params_msg}) ok.")

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
        updated_at=datetime.utcnow().astimezone(),
    ) -> None:
        query, args = get_update_user_query_by_uid(
            uid=uid,
            username=username,
            nickname=nickname,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=is_admin,
            extra=extra,
            updated_at=updated_at,
        )
        await self.execute(query, *args)
        params_msg = f"uid={uid}"
        logger.info(f"update_user_by_uid({params_msg}) ok.")

    @overrides
    async def delete_user_by_uid(self, uid: int) -> None:
        query = SAFE_DELETE_USER_BY_UID.replace("$1", str(uid))
        await self.execute(query)
        params_msg = f"uid={uid}"
        logger.info(f"delete_user_by_uid({params_msg}) ok.")

    @overrides
    async def select_user_username_by_uid(self, uid: int) -> str:
        query = SELECT_USER_USERNAME_BY_UID
        row = await self.fetch_row(query, uid)
        result = row["username"]
        params_msg = f"uid={uid}"
        result_msg = f"username={result}"
        logger.info(f"select_user_username_by_uid({params_msg}) -> {result_msg}")
        return result

    @overrides
    async def select_user_uid_by_username(self, username: str) -> int:
        query = SELECT_USER_UID_BY_USERNAME
        row = await self.fetch_row(query, username)
        params_msg = f"username={username}"
        if not row:
            raise RuntimeError(f"Not found user: {params_msg}")
        result = row["uid"]
        result_msg = f"uid={result}"
        logger.info(f"select_user_uid_by_username({params_msg}) -> {result_msg}")
        return result

    @overrides
    async def select_user_exists_by_username(self, username: str) -> bool:
        query = SELECT_USER_EXISTS_BY_USERNAME
        row = await self.fetch_row(query, username)
        assert row and len(row) == 1
        result = row["exists"]
        assert isinstance(result, bool)
        params_msg = f"username={username}"
        logger.info(f"select_user_exists_by_username({params_msg}) -> {result}")
        return result

    @overrides
    async def select_user_password_and_salt_by_uid(self, uid: int) -> PassInfo:
        query = SELECT_USER_PASSWORD_AND_SALT_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found user: {params_msg}")
        assert len(row) == 2
        logger.info(f"select_user_password_and_salt_by_uid({params_msg}) ok.")
        return PassInfo(**dict(row))

    @overrides
    async def select_user_extra_by_uid(self, uid: int) -> Any:
        query = SELECT_USER_EXTRA_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found user: {params_msg}")
        assert len(row) == 1
        result = row.get("extra", None)
        logger.info(f"select_user_extra_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_user_by_uid(self, uid: int) -> User:
        query = SELECT_USER_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found user: {params_msg}")
        result = User(**dict(row))
        logger.info(f"select_user_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def select_users(self) -> List[User]:
        result: List[User] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_USER_ALL
                async for row in conn.cursor(query):
                    result.append(User(**dict(row)))
        result_msg = f"{len(result)} users"
        logger.info(f"select_users() -> {result_msg}")
        return result

    @overrides
    async def select_users_count(self) -> int:
        query = SELECT_USER_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = row.get("count", 0)
        assert isinstance(result, int)
        logger.info(f"select_users_count() -> {result}")
        return result

    @overrides
    async def select_admin_count(self) -> int:
        query = SELECT_USER_ADMIN_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = row.get("count", 0)
        assert isinstance(result, int)
        logger.info(f"select_admin_count() -> {result}")
        return result

    @overrides
    async def select_exists_admin_user(self) -> bool:
        query = SELECT_USER_ADMIN_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = bool(row.get("count", 0) >= 1)
        logger.info(f"select_exists_admin_user() -> {result}")
        return result

    @overrides
    async def select_user_username(self) -> List[str]:
        result: List[str] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_USER_USERNAME
                async for row in conn.cursor(query):
                    result.append(row["username"])
        result_msg = f"{len(result)} users"
        logger.info(f"select_user_username() -> {result_msg}")
        return result
