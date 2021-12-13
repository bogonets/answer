# -*- coding: utf-8 -*-

from typing import Optional
from recc.database.interfaces.db_interface import DbInterface
from recc.database.postgresql.mixin.pg_daemon import PgDaemon
from recc.database.postgresql.mixin.pg_group import PgGroup
from recc.database.postgresql.mixin.pg_group_member import PgGroupMember
from recc.database.postgresql.mixin.pg_info import PgInfo
from recc.database.postgresql.mixin.pg_layout import PgLayout
from recc.database.postgresql.mixin.pg_open import PgOpen
from recc.database.postgresql.mixin.pg_permission import PgPermission
from recc.database.postgresql.mixin.pg_table import PgTable
from recc.database.postgresql.mixin.pg_port import PgPort
from recc.database.postgresql.mixin.pg_project import PgProject
from recc.database.postgresql.mixin.pg_project_member import PgProjectMember
from recc.database.postgresql.mixin.pg_rule import PgRule
from recc.database.postgresql.mixin.pg_task import PgTask
from recc.database.postgresql.mixin.pg_user import PgUser
from recc.database.postgresql.mixin.pg_utils import PgUtils
from recc.database.postgresql.mixin.pg_widget import PgWidget
from recc.variables.database import DEFAULT_TIMEOUT_SECONDS

EX_KEY_TIMEOUT = "timeout"


class PgDb(
    DbInterface,
    PgDaemon,
    PgGroup,
    PgGroupMember,
    PgInfo,
    PgLayout,
    PgOpen,
    PgPermission,
    PgPort,
    PgProject,
    PgProjectMember,
    PgRule,
    PgTable,
    PgTask,
    PgUser,
    PgUtils,
    PgWidget,
):
    """
    PostgreSQL Database class.

    :param kwargs:
        - timeout: Optional timeout value in seconds.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        pw: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs,
    ):
        self._pool = None

        self._host = host
        self._port = port
        self._user = user
        self._pw = pw
        self._name = name

        self._timeout = float(kwargs.get(EX_KEY_TIMEOUT, DEFAULT_TIMEOUT_SECONDS))
