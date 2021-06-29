# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from recc.exception.recc_error import ReccNotFoundError
from recc.log.logging import recc_database_logger as logger
from recc.struct.user import User, PassInfo
from recc.database.postgresql.mixin.async_pg_base import AsyncPgBase
from recc.database.postgresql.query.user import (
    INSERT_USER,
    UPDATE_USER_LAST_LOGIN_BY_USERNAME,
    UPDATE_USER_USERNAME_BY_UID,
    UPDATE_USER_PASSWORD_AND_SALT_BY_UID,
    UPDATE_USER_PASSWORD_AND_SALT_BY_USERNAME,
    UPDATE_USER_EXTRA_BY_UID,
    UPDATE_USER_EXTRA_BY_USERNAME,
    DELETE_USER_BY_UID,
    DELETE_USER_BY_USERNAME,
    SELECT_USER_ADMIN_COUNT,
    SELECT_USER_UID_BY_USERNAME,
    SELECT_USER_PASSWORD_AND_SALT_BY_USERNAME,
    SELECT_USER_BY_USERNAME,
    SELECT_USER_EXTRA_BY_USERNAME,
    SELECT_USER_ALL,
    get_update_user_query_by_username,
)


class AsyncPgUser(AsyncPgBase):
    async def create_user(
        self,
        username: str,
        password: str,
        salt: str,
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
        logger.info(f"create_user({params_msg}) ok.")

    async def update_user_last_login_by_username(
        self, username: str, last_login=datetime.utcnow()
    ) -> None:
        query = UPDATE_USER_LAST_LOGIN_BY_USERNAME
        await self.execute(query, username, last_login)
        params_msg = f"username={username},last_login={last_login}"
        logger.info(f"update_user_last_login_by_username({params_msg}) ok.")

    async def update_user_username_by_uid(
        self, uid: int, username: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_USER_USERNAME_BY_UID
        await self.execute(query, uid, username, updated_at)
        params_msg = f"uid={uid},username={username}"
        logger.info(f"update_user_username_by_uid({params_msg}) ok.")

    async def update_user_password_and_salt_by_uid(
        self, uid: int, password: str, salt: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_USER_PASSWORD_AND_SALT_BY_UID
        await self.execute(query, uid, password, salt, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_user_password_and_salt_by_uid({params_msg}) ok.")

    async def update_user_password_and_salt_by_username(
        self, username: str, password: str, salt: str, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_USER_PASSWORD_AND_SALT_BY_USERNAME
        await self.execute(query, username, password, salt, updated_at)
        params_msg = f"username={username}"
        logger.info(f"update_user_password_and_salt_by_username({params_msg}) ok.")

    async def update_user_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_USER_EXTRA_BY_UID
        await self.execute(query, uid, extra, updated_at)
        params_msg = f"uid={uid}"
        logger.info(f"update_user_extra_by_uid({params_msg}) ok.")

    async def update_user_extra_by_username(
        self, username: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        query = UPDATE_USER_EXTRA_BY_USERNAME
        await self.execute(query, username, extra, updated_at)
        params_msg = f"username={username}"
        logger.info(f"update_user_extra_by_username({params_msg}) ok.")

    async def update_user_by_username(
        self,
        username: str,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin: Optional[bool] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        query, args = get_update_user_query_by_username(
            username=username,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=is_admin,
            extra=extra,
            updated_at=updated_at,
        )
        await self.execute(query, *args)
        params_msg = f"username={username}"
        logger.info(f"update_user_by_username({params_msg}) ok.")

    async def delete_user_by_uid(self, uid: int) -> None:
        query = DELETE_USER_BY_UID
        await self.execute(query, uid)
        params_msg = f"uid={uid}"
        logger.info(f"delete_user_by_uid({params_msg}) ok.")

    async def delete_user_by_name(self, username: str) -> None:
        query = DELETE_USER_BY_USERNAME
        await self.execute(query, username)
        params_msg = f"username={username}"
        logger.info(f"delete_user_by_name({params_msg}) ok.")

    async def get_user_uid_by_username(self, username: str) -> int:
        query = SELECT_USER_UID_BY_USERNAME
        row = await self.fetch_row(query, username)
        result = row["uid"]
        params_msg = f"username={username}"
        result_msg = f"uid={result}"
        logger.info(f"get_user_uid_by_username({params_msg}) -> {result_msg}")
        return result

    async def exist_user(self, username: str) -> bool:
        query = SELECT_USER_UID_BY_USERNAME
        row = await self.fetch_row(query, username)
        result = bool(row and len(row) == 1)
        params_msg = f"username={username}"
        logger.info(f"exist_user({params_msg}) -> {result}")
        return result

    async def get_user_password_and_salt(self, username: str) -> PassInfo:
        query = SELECT_USER_PASSWORD_AND_SALT_BY_USERNAME
        row = await self.fetch_row(query, username)
        params_msg = f"username={username}"
        if not row:
            raise ReccNotFoundError(f"Not found user: {params_msg}")
        assert len(row) == 2
        logger.info(f"get_user_password_and_salt({params_msg}) ok.")
        return PassInfo(**dict(row))

    async def get_user_extra(self, username: str) -> Any:
        query = SELECT_USER_EXTRA_BY_USERNAME
        row = await self.fetch_row(query, username)
        params_msg = f"username={username}"
        if not row:
            raise ReccNotFoundError(f"Not found user: {params_msg}")
        assert len(row) == 1
        result = row.get("extra", None)
        logger.info(f"get_user_extra({params_msg}) ok.")
        return result

    async def get_user_by_username(self, username: str) -> User:
        query = SELECT_USER_BY_USERNAME
        row = await self.fetch_row(query, username)
        params_msg = f"username={username}"
        if not row:
            raise ReccNotFoundError(f"Not found user: {params_msg}")
        assert len(row) == 9
        result = User(**dict(row))
        result.username = username
        logger.info(f"get_user_by_username({params_msg}) ok.")
        return result

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

    async def exist_admin_user(self) -> bool:
        query = SELECT_USER_ADMIN_COUNT
        row = await self.fetch_row(query)
        assert row and len(row) == 1
        result = bool(row.get("count", 0) >= 1)
        logger.info(f"exist_admin_user() -> {result}")
        return result
