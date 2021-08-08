# -*- coding: utf-8 -*-

from typing import Any, List, Iterable, Optional
from datetime import datetime
from recc.session.session import Session
from recc.database.struct.user import User
from recc.database.struct.group import Group
from recc.database.struct.project import Project


class HttpSession:

    session: Session
    user: User
    groups: List[Group]
    projects: List[Project]

    def __init__(
        self,
        session: Session,
        user: User,
        groups: Optional[Iterable[Group]] = None,
        projects: Optional[Iterable[Project]] = None,
    ):
        self.session = session
        self.user = user
        self.groups = list(groups if groups else [])
        self.projects = list(projects if projects else [])
        self._validation()

    def _validation(self) -> None:
        assert self.user.uid is not None  # `uid` can be 0
        assert self.user.username  # Database cascade: NOT NULL
        assert self.user.created_at  # Database cascade: NOT NULL

    @property
    def issuer(self) -> str:
        return self.session.issuer

    @property
    def audience(self) -> str:
        return self.session.audience

    @property
    def expiration_time(self) -> datetime:
        return self.session.expiration_time

    @property
    def issued_at(self) -> datetime:
        return self.session.issued_at

    @property
    def uid(self) -> int:
        assert self.user.uid is not None
        return self.user.uid

    @property
    def username(self) -> str:
        assert self.user.username
        return self.user.username

    @property
    def nickname(self) -> str:
        return self.user.nickname if self.user.nickname else ""

    @property
    def email(self) -> str:
        return self.user.email if self.user.email else ""

    @property
    def phone1(self) -> str:
        return self.user.phone1 if self.user.phone1 else ""

    @property
    def phone2(self) -> str:
        return self.user.phone2 if self.user.phone2 else ""

    @property
    def is_admin(self) -> bool:
        return self.user.is_admin if self.user.is_admin else False

    @property
    def extra(self) -> Any:
        return self.user.extra

    @property
    def created_at(self) -> datetime:
        assert self.user.created_at
        return self.user.created_at

    @property
    def updated_at(self) -> datetime:
        if self.user.updated_at:
            return self.user.updated_at
        else:
            return self.created_at

    @property
    def last_login(self) -> datetime:
        if self.user.last_login:
            return self.user.last_login
        else:
            return self.created_at
