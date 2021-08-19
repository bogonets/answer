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
    DELETE_USER_BY_UID,
    SELECT_USER_ADMIN_COUNT,
    SELECT_USER_COUNT,
    SELECT_USER_USERNAME_BY_UID,
    SELECT_USER_UID_BY_USERNAME,
    EXISTS_USER_BY_USERNAME,
    SELECT_USER_PASSWORD_AND_SALT_BY_UID,
    SELECT_USER_BY_UID,
    SELECT_USER_EXTRA_BY_UID,
    SELECT_USER_ALL,
    get_update_user_query_by_uid,
)


class PgUser(DbUser, PgBase):
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
        created_at=datetime.utcnow(),
    ) -> None:
        query = INSERT_USER
        await self.execute(
            query,
            username,
            password,
            salt,
            nickname,
            email,
            phone1,
            phone2,
            is_admin,
            extra,
            created_at,
        )
        params_msg = f"username={username}"
        if is_admin:
            params_msg += ",admin"
        logger.info(f"insert_user({params_msg}) ok.")

    @overrides
    async def update_user_last_login_by_uid(
        self, uid: int, last_login=datetime.utcnow()
    ) -> None:
        query = UPDATE_USER_LAST_LOGIN_BY_UID
        await self.execute(query, uid, last_login)
        params_msg = f"uid={uid},last_login={last_login}"
        logger.info(f"update_user_last_login_by_uid({params_msg}) ok.")

    @overrides
    async def update_user_password_and_salt_by_uid(
        self, uid: int, password: str, salt: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_USER_PASSWORD_AND_SALT_BY_UID
        await self.execute(query, uid, password, salt, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_user_password_and_salt_by_uid({params_msg}) ok.")

    @overrides
    async def update_user_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
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
        updated_at=datetime.utcnow(),
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
        query = DELETE_USER_BY_UID
        await self.execute(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"delete_user_by_uid({params_msg}) ok.")

    @overrides
    async def get_user_username_by_uid(self, uid: int) -> str:
        query = SELECT_USER_USERNAME_BY_UID
        row = await self.fetch_row(query, uid)
        result = row["username"]
        params_msg = f"uid={uid}"
        result_msg = f"username={result}"
        logger.info(f"get_user_username_by_uid({params_msg}) -> {result_msg}")
        return result

    @overrides
    async def get_user_uid_by_username(self, username: str) -> int:
        query = SELECT_USER_UID_BY_USERNAME
        row = await self.fetch_row(query, username)
        result = row["uid"]
        params_msg = f"username={username}"
        result_msg = f"uid={result}"
        logger.info(f"get_user_uid_by_username({params_msg}) -> {result_msg}")
        return result

    @overrides
    async def exist_user_by_username(self, username: str) -> bool:
        query = EXISTS_USER_BY_USERNAME
        row = await self.fetch_row(query, username)
        result = row["exists"]
        assert isinstance(result, bool)
        params_msg = f"username={username}"
        logger.info(f"exist_user_by_username({params_msg}) -> {result}")
        return result

    @overrides
    async def get_user_password_and_salt_by_uid(self, uid: int) -> PassInfo:
        query = SELECT_USER_PASSWORD_AND_SALT_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found user: {params_msg}")
        assert len(row) == 2
        logger.info(f"get_user_password_and_salt_by_uid({params_msg}) ok.")
        return PassInfo(**dict(row))

    @overrides
    async def get_user_extra_by_uid(self, uid: int) -> Any:
        query = SELECT_USER_EXTRA_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found user: {params_msg}")
        assert len(row) == 1
        result = row.get("extra", None)
        logger.info(f"get_user_extra_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def get_user_by_uid(self, uid: int) -> User:
        query = SELECT_USER_BY_UID
        row = await self.fetch_row(query, uid)
        params_msg = f"uid={uid}"
        if not row:
            raise RuntimeError(f"Not found user: {params_msg}")
        result = User(**dict(row))
        logger.info(f"get_user_by_uid({params_msg}) ok.")
        return result

    @overrides
    async def get_users(self) -> List[User]:
        result: List[User] = list()
        async with self.conn() as conn:
            async with conn.transaction():
                query = SELECT_USER_ALL
                async for row in conn.cursor(query):
                    result.append(User(**dict(row)))
        result_msg = f"{len(result)} users"
        logger.info(f"get_users() -> {result_msg}")
        return result

    @overrides
    async def get_users_count(self) -> int:
        query = SELECT_USER_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = int(row.get("count", 0))
        logger.info(f"get_users_count() -> {result}")
        return result

    @overrides
    async def get_admin_count(self) -> int:
        query = SELECT_USER_ADMIN_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = int(row.get("count", 0))
        logger.info(f"get_admin_count() -> {result}")
        return result

    @overrides
    async def exists_admin_user(self) -> bool:
        query = SELECT_USER_ADMIN_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = bool(row.get("count", 0) >= 1)
        logger.info(f"exist_admin_user() -> {result}")
        return result
