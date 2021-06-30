# -*- coding: utf-8 -*-

import os
from typing import Optional, List, Tuple, Any

from recc.crypto.password import encrypt_password
from recc.session.session import Session
from recc.exception.recc_error import ReccArgumentError, ReccAuthError
from recc.struct.user import User
from recc.core.mixin.context_base import ContextBase
from recc.variables.database import (
    PASSWORD_HEX_STR_SIZE,
    SALT_BYTE,
    SALT_HEX_STR_SIZE,
)


class ContextUser(ContextBase):
    async def exist_admin_user(self) -> bool:
        return await self.database.exist_admin_user()

    async def signup(
        self,
        user_id: str,
        hashed_user_pw: str,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin=False,
    ) -> None:
        if not user_id:
            raise ReccArgumentError("User ID is required.")

        if len(hashed_user_pw) != PASSWORD_HEX_STR_SIZE:
            msg1 = f"Password({hashed_user_pw})"
            msg2 = f"length is not {PASSWORD_HEX_STR_SIZE} characters."
            raise ReccArgumentError(f"{msg1} {msg2}")

        salt = os.urandom(SALT_BYTE)
        salted_password = encrypt_password(hashed_user_pw, salt)

        db_pw = salted_password.hex()
        assert len(db_pw) == PASSWORD_HEX_STR_SIZE

        db_salt = salt.hex()
        assert len(db_salt) == SALT_HEX_STR_SIZE

        return await self.database.create_user(
            user_id,
            db_pw,
            db_salt,
            email=email,
            phone1=phone1,
            phone2=phone2,
            is_admin=is_admin,
        )

    async def signup_admin(self, user_id: str, hashed_user_pw: str) -> None:
        await self.signup(user_id, hashed_user_pw, is_admin=True)

    async def login(self, username: str, hashed_user_pw: str) -> Tuple[str, str]:
        if not username:
            raise ReccArgumentError("User ID is required.")

        if len(hashed_user_pw) != PASSWORD_HEX_STR_SIZE:
            msg1 = f"Password({hashed_user_pw})"
            msg2 = f"length is not {PASSWORD_HEX_STR_SIZE} characters."
            raise ReccArgumentError(f"{msg1} {msg2}")

        saved_pass = await self.database.get_user_password_and_salt(username)
        saved_password = saved_pass.password
        saved_salt = saved_pass.salt
        salt = bytes.fromhex(saved_salt)
        salted_password = encrypt_password(hashed_user_pw, salt)

        if saved_password != salted_password.hex():
            raise ReccAuthError("The password is incorrect.")

        await self.database.update_user_last_login_by_username(username)
        return self.session_factory.create_tokens(username)

    async def remove_user(self, username: str) -> None:
        # TODO: Remove related datas. e.g. group_member, project_member
        await self.database.delete_user_by_name(username)

    async def update_user(
        self,
        username: str,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        extra: Optional[Any] = None,
    ) -> None:
        await self.database.update_user_by_username(
            username, email=email, phone1=phone1, phone2=phone2, extra=extra
        )

    async def renew_access_token(self, token: str) -> str:
        return self.session_factory.renew_access_token(token)

    async def get_access_session(self, token: str) -> Session:
        return self.session_factory.decode_access(token)

    async def get_user(self, session: Session, username: str) -> User:
        user = await self.database.get_user_by_username(session.audience)
        if session.audience == username:
            return user
        if not user.is_admin:
            raise PermissionError("Permission denied")
        return await self.database.get_user_by_username(username)

    async def get_users(self, session: Session) -> List[User]:
        user = await self.database.get_user_by_username(session.audience)
        if not user.is_admin:
            raise PermissionError("Permission denied")
        return await self.database.get_users()

    async def exist_user(self, session: Session, test_username: str) -> bool:
        user = await self.database.get_user_by_username(session.audience)
        if not user.is_admin:
            raise PermissionError("Permission denied")
        return await self.database.exist_user(test_username)
