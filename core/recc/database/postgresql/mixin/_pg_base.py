# -*- coding: utf-8 -*-

from typing import Optional, Any, Type, List
from asyncpg import InvalidCatalogNameError, create_pool, connect
from overrides import overrides
from asyncpg.pool import Pool, PoolAcquireContext
from asyncpg.connection import Connection
from asyncpg.protocol import Record
from recc.driver.json import global_json_encoder, global_json_decoder
from recc.database.interfaces.db_base_interface import RecordType, ColumnType
from recc.database.interfaces.db_base import DbBase

_DEFAULT_TEMPLATE_DATABASE = "template1"


class PgConnection:
    """
    Implementation for Type Hinting.
    """

    __slots__ = ("_pool", "_conn", "_timeout")

    def __init__(self, pool: Pool, timeout: Optional[float] = None):
        assert pool is not None
        self._pool = pool
        self._conn: Optional[PoolAcquireContext] = None
        self._timeout = timeout

    async def __aenter__(self) -> Connection:
        conn = await self._pool.acquire(timeout=self._timeout)
        self._conn = conn
        return self._conn

    async def __aexit__(self, exc_type, exc_value, tb):
        await self._pool.release(self._conn)


async def _init_connection(conn: Connection):
    await conn.set_type_codec(
        "jsonb",
        schema="pg_catalog",
        encoder=global_json_encoder,
        decoder=global_json_decoder,
        format="text",
    )


async def connect_and_create_if_not_exists(
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
    command_timeout: Optional[float] = None,
    min_size=10,
    max_size=10,
    max_queries=50000,
    max_inactive_connection_lifetime=300.0,
) -> Pool:
    try:
        pool = await create_pool(
            min_size=min_size,
            max_size=max_size,
            max_queries=max_queries,
            max_inactive_connection_lifetime=max_inactive_connection_lifetime,
            setup=None,
            init=_init_connection,
            loop=None,
            connection_class=Connection,
            record_class=Record,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            command_timeout=command_timeout,
        )
        return pool
    except InvalidCatalogNameError:
        # Database does not exist, create it.
        pass

    sys_conn = await connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=_DEFAULT_TEMPLATE_DATABASE,
        command_timeout=command_timeout,
    )
    await sys_conn.execute(f'CREATE DATABASE "{database}" OWNER "{user}";')
    await sys_conn.close()

    # Connect to the newly created database.
    return await create_pool(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        command_timeout=command_timeout,
        init=_init_connection,
    )


async def drop_database(
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
) -> None:
    conn = await connect(host=host, port=port, user=user, password=password)
    await conn.execute(f'DROP DATABASE "{database}";')
    await conn.close()


class PgBase(DbBase):

    _pool: Optional[Pool] = None
    _host: Optional[str] = None
    _port: Optional[int] = None
    _user: Optional[str] = None
    _pw: Optional[str] = None
    _name: Optional[str] = None
    _timeout: Optional[float] = None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def user(self):
        return self._user

    @property
    def name(self):
        return self._name

    @property
    def timeout(self):
        return self._timeout

    @overrides
    def is_open(self) -> bool:
        return self._pool is not None

    @overrides
    async def open(self) -> None:
        self._pool = await connect_and_create_if_not_exists(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._pw,
            database=self._name,
            command_timeout=self._timeout,
        )

    @overrides
    async def close(self) -> None:
        assert self._pool is not None
        await self._pool.close()
        self._pool = None

    @overrides
    async def drop_database(self) -> None:
        await drop_database(
            self._host,
            self._port,
            self._user,
            self._pw,
            self._name,
        )

    def conn(self) -> PgConnection:
        assert self._pool is not None
        return PgConnection(self._pool)

    @overrides
    async def execute(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        async with self.conn() as conn:
            await conn.execute(query, *args, timeout=timeout)

    @overrides
    async def fetch_rows(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        async with self.conn() as conn:
            return await conn.fetch(query, *args, timeout=timeout)

    @overrides
    async def fetch_first_row(
        self,
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> Any:
        async with self.conn() as conn:
            return await conn.fetchrow(query, *args, timeout=timeout)

    @overrides
    async def fetch_first_row_column(
        self,
        query: str,
        *args,
        column=0,
        timeout: Optional[float] = None,
    ) -> Any:
        async with self.conn() as conn:
            return await conn.fetchval(query, *args, column=column, timeout=timeout)

    @overrides
    async def rows(
        self,
        cls: Type[RecordType],
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> List[RecordType]:
        rows = await self.fetch_rows(query, *args, timeout=timeout)
        if rows is not None:
            return [cls(**row) for row in rows]
        else:
            return list()

    @overrides
    async def row(
        self,
        cls: Type[RecordType],
        query: str,
        *args,
        timeout: Optional[float] = None,
    ) -> RecordType:
        row = await self.fetch_first_row(query, *args, timeout=timeout)
        if row is None:
            raise LookupError("The query result does not exist")
        return cls(**row)

    @overrides
    async def column(
        self,
        cls: Type[ColumnType],
        query: str,
        *args,
        column=0,
        timeout: Optional[float] = None,
    ) -> ColumnType:
        value = await self.fetch_first_row_column(
            query, *args, column=column, timeout=timeout
        )
        if value is None:
            raise LookupError("The query result does not exist")
        if not isinstance(value, cls):
            raise TypeError(f"The result is not of the '{cls.__name__}' type")
        return value
