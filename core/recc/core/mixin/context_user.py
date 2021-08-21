# -*- coding: utf-8 -*-

from os import urandom
from typing import Optional, List, Tuple, Any
from recc.crypto.password import encrypt_password
from recc.session.session import Session
from recc.database.struct.user import PassInfo, User
from recc.core.mixin.context_base import ContextBase
from recc.variables.database import (
    PASSWORD_HEX_STR_SIZE,
    SALT_BYTE,
    SALT_HEX_STR_SIZE,
)


def salting_password(hashed_password: str) -> PassInfo:
    if len(hashed_password) != PASSWORD_HEX_STR_SIZE:
        msg1 = f"Password('{hashed_password}')"
        msg2 = f"length is not {PASSWORD_HEX_STR_SIZE} characters."
        raise ValueError(f"{msg1} {msg2}")

    salt = urandom(SALT_BYTE)
    salted_password = encrypt_password(hashed_password, salt)

    db_pw = salted_password.hex()
    assert len(db_pw) == PASSWORD_HEX_STR_SIZE
    assert db_pw == db_pw.strip()

    db_salt = salt.hex()
    assert len(db_salt) == SALT_HEX_STR_SIZE
    assert db_salt == db_salt.strip()

    return PassInfo(db_pw, db_salt, strip=False)


class ContextUser(ContextBase):

    _already_admin_user = False

    async def exists_admin_user(self) -> bool:
        # After being created in the DB, there is no scenario that can be removed.
        if self._already_admin_user:
            return True
        self._already_admin_user = await self.database.select_exists_admin_user()
        return self._already_admin_user

    async def get_admin_count(self) -> int:
        return await self.database.select_admin_count()

    async def signup(
        self,
        username: str,
        hashed_password: str,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin=False,
        extra: Optional[Any] = None,
    ) -> int:
        if not username:
            raise ValueError("The `username` argument is empty.")
        pass_info = salting_password(hashed_password)
        return await self.database.insert_user(
            username,
            pass_info.password,
            pass_info.salt,
            nickname=nickname,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=is_admin,
            extra=extra,
        )

    async def signup_guest(
        self,
        username: str,
        hashed_password: str,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
    ) -> None:
        await self.signup(
            username=username,
            hashed_password=hashed_password,
            nickname=nickname,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=False,
        )

    async def signup_admin(self, username: str, hashed_password: str) -> None:
        await self.signup(username, hashed_password, is_admin=True)

    async def challenge_password(self, username: str, hashed_password: str) -> bool:
        if not username:
            raise ValueError("The `username` argument is empty.")

        if len(hashed_password) != PASSWORD_HEX_STR_SIZE:
            msg1 = f"Password('{hashed_password}')"
            msg2 = f"length is not {PASSWORD_HEX_STR_SIZE} characters."
            raise ValueError(f"{msg1} {msg2}")

        user_uid = await self.get_user_uid(username)
        if user_uid is None:
            raise RuntimeError(f"Not found user: {username}")
        saved_pass = await self.database.select_user_password_and_salt_by_uid(user_uid)
        saved_password = saved_pass.password
        saved_salt = saved_pass.salt
        salt = bytes.fromhex(saved_salt)
        salted_password = encrypt_password(hashed_password, salt)

        return saved_password == salted_password.hex()

    async def signin(self, username: str) -> Tuple[str, str]:
        user_uid = await self.get_user_uid(username)
        await self.database.update_user_last_login_by_uid(user_uid)
        return self.session_factory.create_tokens(username)

    async def change_password(self, username: str, hashed_password: str) -> None:
        user_uid = await self.get_user_uid(username)
        pass_info = salting_password(hashed_password)
        await self.database.update_user_password_and_salt_by_uid(
            user_uid, pass_info.password, pass_info.salt
        )

    async def remove_user(self, username: str) -> None:
        user_uid = await self.get_user_uid(username)
        await self.database.delete_user_by_uid(user_uid)

    async def update_user(
        self,
        uid: int,
        username: Optional[str] = None,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin: Optional[bool] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_user_by_uid(
            uid=uid,
            username=username,
            nickname=nickname,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=is_admin,
            extra=extra,
        )

    async def update_user_extra(self, username: str, extra: Any) -> None:
        user_uid = await self.get_user_uid(username)
        await self.database.update_user_extra_by_uid(user_uid, extra)

    async def renew_access_token(self, token: str) -> str:
        return self.session_factory.renew_access_token(token)

    async def get_access_session(self, token: str) -> Session:
        return self.session_factory.decode_access(token)

    async def get_user(self, uid: int, remove_sensitive=True) -> User:
        result = await self.database.select_user_by_uid(uid)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_users(self, remove_sensitive=True) -> List[User]:
        result = list()
        for user in await self.database.select_users():
            if remove_sensitive:
                user.remove_sensitive()
            result.append(user)
        return result

    async def exist_user(self, username: str) -> bool:
        # Do not use cache's uid.
        return await self.database.select_user_exists_by_username(username)
