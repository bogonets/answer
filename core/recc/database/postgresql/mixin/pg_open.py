# -*- coding: utf-8 -*-

from overrides import overrides
from recc.database.interfaces.db_open import DbOpen
from recc.database.postgresql.mixin.pg_base import PgBase
from recc.database.postgresql.pg_utils import (
    connect_and_create_if_not_exists,
    drop_database,
)


class PgOpen(DbOpen, PgBase):
    @overrides
    def is_open(self) -> bool:
        return self._pool is not None

    @overrides
    async def open(self) -> None:
        self._pool = await connect_and_create_if_not_exists(
            host=self._db_host,
            port=self._db_port,
            user=self._db_user,
            password=self._db_pw,
            database=self._db_name,
            command_timeout=self._timeout,
        )

    @overrides
    async def close(self) -> None:
        assert self._pool
        await self._pool.close()
        self._pool = None

    @overrides
    async def drop(self) -> None:
        await drop_database(
            self._db_host,
            self._db_port,
            self._db_user,
            self._db_pw,
            self._db_name,
        )
