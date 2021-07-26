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
    db_host: Optional[str] = None,
    db_port: Optional[int] = None,
    db_user: Optional[str] = None,
    db_pw: Optional[str] = None,
    db_name: Optional[str] = None,
    **kwargs,
) -> DbInterface:
    if db_type == DB_TYPE_NAME_MYSQL:
        raise NotImplementedError("MySQL database type is not supported.")
    elif db_type == DB_TYPE_NAME_SQLITE:
        raise NotImplementedError("SQLite database type is not supported.")
    elif db_type == DB_TYPE_NAME_POSTGRES:
        return PgDb(db_host, db_port, db_user, db_pw, db_name, **kwargs)
    else:
        raise ValueError(f"Unknown database-manager type: {db_type}")
