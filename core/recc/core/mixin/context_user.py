# -*- coding: utf-8 -*-

import os
from typing import Optional, List, Tuple, Any
from recc.crypto.password import encrypt_password
from recc.session.session import Session
from recc.database.struct.user import PassInfo, User
from recc.core.mixin.context_base import ContextBase
from recc.packet.signup import SignupQ
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

    salt = os.urandom(SALT_BYTE)
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
        self._already_admin_user = await self.database.exists_admin_user()
        return self._already_admin_user

    async def get_admin_count(self) -> int:
        return await self.database.get_admin_count()

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
    ) -> None:
        if not username:
            raise ValueError("The `username` argument is empty.")
        pass_info = salting_password(hashed_password)
        return await self.database.create_user(
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

    async def signup_guest(self, request: SignupQ) -> None:
        await self.signup(
            username=request.username,
            hashed_password=request.password,
            nickname=request.nickname,
            email=request.email,
            phone1=request.phone1,
            phone2=request.phone2,
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

        saved_pass = await self.database.get_user_password_and_salt(username)
        saved_password = saved_pass.password
        saved_salt = saved_pass.salt
        salt = bytes.fromhex(saved_salt)
        salted_password = encrypt_password(hashed_password, salt)

        return saved_password == salted_password.hex()

    async def signin(self, username: str) -> Tuple[str, str]:
        if not username:
            raise ValueError("The `username` argument is empty.")

        await self.database.update_user_last_login_by_username(username)
        return self.session_factory.create_tokens(username)

    async def login(self, username: str) -> Tuple[str, str]:
        if not username:
            raise ValueError("The `username` argument is empty.")

        return await self.signin(username)

    async def change_password(self, username: str, hashed_password: str) -> None:
        if not username:
            raise ValueError("The `username` argument is empty.")

        pass_info = salting_password(hashed_password)
        await self.database.update_user_password_and_salt_by_username(
            username, pass_info.password, pass_info.salt
        )

    async def remove_user(self, username: str) -> None:
        if not username:
            raise ValueError("The `username` argument is empty.")

        # TODO: Remove related datas. e.g. group_member, project_member
        await self.database.delete_user_by_name(username)

    async def update_user(
        self,
        username: str,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin: Optional[bool] = None,
        extra: Optional[Any] = None,
    ) -> None:
        if not username:
            raise ValueError("The `username` argument is empty.")

        await self.database.update_user_by_username(
            username,
            nickname=nickname,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=is_admin,
            extra=extra,
        )

    async def update_user_extra(self, username: str, extra: Any) -> None:
        if not username:
            raise ValueError("The `username` argument is empty.")

        await self.database.update_user_extra_by_username(username, extra)

    async def renew_access_token(self, token: str) -> str:
        return self.session_factory.renew_access_token(token)

    async def get_access_session(self, token: str) -> Session:
        return self.session_factory.decode_access(token)

    async def get_user_uid(self, username: str) -> int:
        if not username:
            raise ValueError("The `username` argument is empty.")

        return await self.database.get_user_uid_by_username(username)

    async def get_user(self, username: str, remove_sensitive=True) -> User:
        if not username:
            raise ValueError("The `username` argument is empty.")

        result = await self.database.get_user_by_username(username)
        if remove_sensitive:
            result.remove_sensitive()
        return result

    async def get_self(self, session: Session, remove_sensitive=True) -> User:
        return await self.get_user(session.audience, remove_sensitive)

    async def get_user_extra(self, username: str) -> Any:
        if not username:
            raise ValueError("The `username` argument is empty.")
        return await self.database.get_user_extra(username)

    async def get_self_extra(self, session: Session) -> Any:
        return await self.get_user_extra(session.audience)

    async def get_users(self, remove_sensitive=True) -> List[User]:
        result = list()
        for user in await self.database.get_users():
            if remove_sensitive:
                user.remove_sensitive()
            result.append(user)
        return result

    async def exist_user(self, username: str) -> bool:
        if not username:
            raise ValueError("The `username` argument is empty.")

        return await self.database.exist_user(username)
