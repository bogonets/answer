# -*- coding: utf-8 -*-

from typing import Optional
from recc.database.postgresql.mixin._pg_base import PgBase  # noqa


class PgCommon(PgBase):
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        pw: Optional[str] = None,
        name: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self._pool = None
        self._host = host
        self._port = port
        self._user = user
        self._pw = pw
        self._name = name
        self._timeout = timeout
