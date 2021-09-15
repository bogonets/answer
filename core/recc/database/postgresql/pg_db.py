# -*- coding: utf-8 -*-

from typing import Optional
from recc.database.interfaces.db_interface import DbInterface
from recc.database.postgresql.mixin.pg_group import PgGroup
from recc.database.postgresql.mixin.pg_group_member import PgGroupMember
from recc.database.postgresql.mixin.pg_info import PgInfo
from recc.database.postgresql.mixin.pg_layout import PgLayout
from recc.database.postgresql.mixin.pg_misc import PgMisc
from recc.database.postgresql.mixin.pg_open import PgOpen
from recc.database.postgresql.mixin.pg_permission import PgPermission
from recc.database.postgresql.mixin.pg_port import PgPort
from recc.database.postgresql.mixin.pg_project import PgProject
from recc.database.postgresql.mixin.pg_project_member import PgProjectMember
from recc.database.postgresql.mixin.pg_task import PgTask
from recc.database.postgresql.mixin.pg_user import PgUser
from recc.database.postgresql.mixin.pg_utils import PgUtils
from recc.database.postgresql.mixin.pg_widget import PgWidget
from recc.variables.database import DEFAULT_TIMEOUT_SECONDS

EX_KEY_TIMEOUT = "timeout"


class PgDb(
    DbInterface,
    PgGroup,
    PgGroupMember,
    PgInfo,
    PgLayout,
    PgMisc,
    PgOpen,
    PgPermission,
    PgPort,
    PgProject,
    PgProjectMember,
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
        db_host: Optional[str] = None,
        db_port: Optional[int] = None,
        db_user: Optional[str] = None,
        db_pw: Optional[str] = None,
        db_name: Optional[str] = None,
        **kwargs,
    ):
        self._pool = None

        self._db_host = db_host
        self._db_port = db_port
        self._db_user = db_user
        self._db_pw = db_pw
        self._db_name = db_name

        self._timeout = float(kwargs.get(EX_KEY_TIMEOUT, DEFAULT_TIMEOUT_SECONDS))

        self._anonymous_group_uid = None
        self._guest_permission_uid = None
        self._reporter_permission_uid = None
        self._operator_permission_uid = None
        self._maintainer_permission_uid = None
