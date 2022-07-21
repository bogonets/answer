# -*- coding: utf-8 -*-

from datetime import datetime

from recc.session.session import Session


class SessionEx:
    def __init__(self, session: Session, uid: int, admin: bool):
        self.session = session
        self.uid = uid
        self.admin = admin

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
