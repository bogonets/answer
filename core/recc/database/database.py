# -*- coding: utf-8 -*-

from typing import Optional
from recc.variables.database import (
    DB_TYPE_NAME_MYSQL,
    DB_TYPE_NAME_POSTGRES,
    DB_TYPE_NAME_SQLITE,
)
from recc.database.interfaces.db_interface import DbInterface
from recc.database.postgresql.pg_db import PgDb


def create_database(
    db_type: str,
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
        raise ValueError(f"Unknown database-manager type: {db_type}")
