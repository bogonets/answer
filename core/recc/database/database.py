# -*- coding: utf-8 -*-

from typing import Optional, Union
from recc.variables.database import (
    DatabaseTypeLiteral,
    DB_TYPE_NAME_MYSQL,
    DB_TYPE_NAME_POSTGRES,
    DB_TYPE_NAME_SQLITE,
    DEFAULT_DATABASE_TYPE,
)
from recc.database.interfaces.db_base import DbBase
from recc.database.interfaces.db_interface import DbInterface
from recc.database.postgresql.pg_db import PgDb
from recc.database.postgresql.pg_common import PgCommon


def create_database(
    db_type: Optional[Union[str, DatabaseTypeLiteral]] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    pw: Optional[str] = None,
    name: Optional[str] = None,
    timeout: Optional[float] = None,
) -> DbInterface:
    t = db_type if db_type else DEFAULT_DATABASE_TYPE
    if t == DB_TYPE_NAME_MYSQL:
        raise NotImplementedError("MySQL database type is not supported.")
    elif t == DB_TYPE_NAME_SQLITE:
        raise NotImplementedError("SQLite database type is not supported.")
    elif t == DB_TYPE_NAME_POSTGRES:
        return PgDb(host, port, user, pw, name, timeout)
    else:
        raise ValueError(f"Unknown database type: {db_type}")


def create_common_database(
    db_type: Optional[Union[str, DatabaseTypeLiteral]] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    pw: Optional[str] = None,
    name: Optional[str] = None,
    timeout: Optional[float] = None,
) -> DbBase:
    t = db_type if db_type else DEFAULT_DATABASE_TYPE
    if t == DB_TYPE_NAME_MYSQL:
        raise NotImplementedError("MySQL database type is not supported.")
    elif t == DB_TYPE_NAME_SQLITE:
        raise NotImplementedError("SQLite database type is not supported.")
    elif t == DB_TYPE_NAME_POSTGRES:
        return PgCommon(host, port, user, pw, name, timeout)
    else:
        raise ValueError(f"Unknown database type: {db_type}")
