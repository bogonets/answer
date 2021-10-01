# -*- coding: utf-8 -*-

from typing import List
from recc.core.mixin.context_base import ContextBase
from recc.packet.environment import EnvironmentA
from recc.packet.system import SystemOverviewA
from recc.system.environ import get_os_envs_dict
from recc.util.python_version import get_python_version_simple


class ContextSystem(ContextBase):
    @staticmethod
    def get_environments() -> List[EnvironmentA]:
        result = list()
        for key, value in get_os_envs_dict().items():
            result.append(EnvironmentA(key, value))
        return result

    async def get_system_overview(self) -> SystemOverviewA:
        users = await self.database.select_users_count()
        groups = await self.database.select_groups_count()
        projects = await self.database.select_projects_count()
        return SystemOverviewA(users, groups, projects)

    @staticmethod
    def get_python_version_info() -> str:
        return get_python_version_simple()
