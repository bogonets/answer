# -*- coding: utf-8 -*-

from typing import Any
from datetime import datetime
from recc.session.session import Session


class SessionEx:
    def __init__(self, session: Session, uid: int, is_admin: bool, extra: Any):
        self.session = session
        self.uid = uid
        self.is_admin = is_admin
        self.extra = extra

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
