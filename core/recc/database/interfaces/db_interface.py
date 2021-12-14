# -*- coding: utf-8 -*-

from abc import ABCMeta
from recc.database.interfaces.db_daemon import DbDaemon
from recc.database.interfaces.db_group import DbGroup
from recc.database.interfaces.db_group_member import DbGroupMember
from recc.database.interfaces.db_info import DbInfo
from recc.database.interfaces.db_layout import DbLayout
from recc.database.interfaces.db_table import DbTable
from recc.database.interfaces.db_open import DbOpen
from recc.database.interfaces.db_permission import DbPermission
from recc.database.interfaces.db_port import DbPort
from recc.database.interfaces.db_project import DbProject
from recc.database.interfaces.db_project_member import DbProjectMember
from recc.database.interfaces.db_role import DbRole
from recc.database.interfaces.db_role_permission import DbRolePermission
from recc.database.interfaces.db_task import DbTask
from recc.database.interfaces.db_user import DbUser
from recc.database.interfaces.db_utils import DbUtils
from recc.database.interfaces.db_widget import DbWidget


class DbInterface(
    DbDaemon,
    DbGroup,
    DbGroupMember,
    DbInfo,
    DbLayout,
    DbOpen,
    DbPermission,
    DbPort,
    DbProject,
    DbProjectMember,
    DbRole,
    DbRolePermission,
    DbTable,
    DbTask,
    DbUser,
    DbUtils,
    DbWidget,
    metaclass=ABCMeta,
):
    pass
