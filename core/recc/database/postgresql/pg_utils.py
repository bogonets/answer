# -*- coding: utf-8 -*-

from typing import Optional
from asyncpg import InvalidCatalogNameError, create_pool, connect
from asyncpg.pool import Pool
from asyncpg.connection import Connection
from recc.driver.json import global_json_encoder, global_json_decoder

_DEFAULT_TEMPLATE_DATABASE = "template1"


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
) -> Pool:
    try:
        pool = await create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            command_timeout=command_timeout,
            init=_init_connection,
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
