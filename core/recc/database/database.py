# -*- coding: utf-8 -*-

from typing import Optional, Union
from recc.variables.database import (
    DatabaseTypeLiteral,
    DB_TYPE_NAME_MYSQL,
    DB_TYPE_NAME_POSTGRES,
    DB_TYPE_NAME_SQLITE,
)
from recc.database.interfaces.db_base import DbBase
from recc.database.interfaces.db_interface import DbInterface
from recc.database.postgresql.pg_db import PgDb
from recc.database.postgresql.pg_common import PgCommon


def create_database(
    db_type: Union[str, DatabaseTypeLiteral],
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    pw: Optional[str] = None,
    name: Optional[str] = None,
    **kwargs,
) -> DbInterface:
    if db_type == DB_TYPE_NAME_MYSQL:
        raise NotImplementedError("MySQL database type is not supported.")
    elif db_type == DB_TYPE_NAME_SQLITE:
        raise NotImplementedError("SQLite database type is not supported.")
    elif db_type == DB_TYPE_NAME_POSTGRES:
        return PgDb(host, port, user, pw, name, **kwargs)
    else:
        raise ValueError(f"Unknown database type: {db_type}")


def create_common_database(
    db_type: Union[str, DatabaseTypeLiteral],
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    pw: Optional[str] = None,
    name: Optional[str] = None,
    **kwargs,
) -> DbBase:
    if db_type == DB_TYPE_NAME_MYSQL:
        raise NotImplementedError("MySQL database type is not supported.")
    elif db_type == DB_TYPE_NAME_SQLITE:
        raise NotImplementedError("SQLite database type is not supported.")
    elif db_type == DB_TYPE_NAME_POSTGRES:
        return PgCommon(host, port, user, pw, name, **kwargs)
    else:
        raise ValueError(f"Unknown database type: {db_type}")
