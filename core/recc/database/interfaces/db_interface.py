# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from recc.database.interfaces.db_base import DbBase
from recc.database.interfaces.db_daemon import DbDaemon
from recc.database.interfaces.db_group import DbGroup
from recc.database.interfaces.db_group_member import DbGroupMember
from recc.database.interfaces.db_info import DbInfo
from recc.database.interfaces.db_layout import DbLayout
from recc.database.interfaces.db_permission import DbPermission
from recc.database.interfaces.db_port import DbPort
from recc.database.interfaces.db_project import DbProject
from recc.database.interfaces.db_project_member import DbProjectMember
from recc.database.interfaces.db_role import DbRole
from recc.database.interfaces.db_role_permission import DbRolePermission
from recc.database.interfaces.db_task import DbTask
from recc.database.interfaces.db_user import DbUser
from recc.database.interfaces.db_widget import DbWidget


class DbInterface(
    DbDaemon,
    DbGroup,
    DbGroupMember,
    DbInfo,
    DbLayout,
    DbPermission,
    DbPort,
    DbProject,
    DbProjectMember,
    DbRole,
    DbRolePermission,
    DbTask,
    DbUser,
    DbWidget,
    metaclass=ABCMeta,
):
    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def drop_database(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create_tables(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def drop_tables(self) -> None:
        raise NotImplementedError


assert not issubclass(DbInterface, DbBase)
assert issubclass(DbInterface, DbDaemon)
assert issubclass(DbInterface, DbGroup)
assert issubclass(DbInterface, DbGroupMember)
assert issubclass(DbInterface, DbInfo)
assert issubclass(DbInterface, DbLayout)
assert issubclass(DbInterface, DbPermission)
assert issubclass(DbInterface, DbPort)
assert issubclass(DbInterface, DbProject)
assert issubclass(DbInterface, DbProjectMember)
assert issubclass(DbInterface, DbRole)
assert issubclass(DbInterface, DbRolePermission)
assert issubclass(DbInterface, DbTask)
assert issubclass(DbInterface, DbUser)
assert issubclass(DbInterface, DbWidget)
