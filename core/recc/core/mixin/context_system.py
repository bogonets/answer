# -*- coding: utf-8 -*-

from typing import Optional, List
from recc.core.mixin.context_base import ContextBase
from recc.chrono.datetime import today
from recc.packet.environment import EnvironmentA
from recc.packet.system import SystemOverviewA
from recc.system.environ import get_os_envs_dict
from recc.util.python_version import get_python_version_simple


class ContextSystem(ContextBase):
    @staticmethod
    def get_environments(startswith: Optional[str] = None) -> List[EnvironmentA]:
        result = list()
        for key, value in get_os_envs_dict().items():
            if startswith is not None and key.startswith(startswith):
                continue
            result.append(EnvironmentA(key, value))
        return result

    async def get_system_overview(self) -> SystemOverviewA:
        time = today()
        users = await self.database.select_users_count()
        groups = await self.database.select_groups_count()
        projects = await self.database.select_projects_count()
        return SystemOverviewA(
            time=time,
            users=users,
            groups=groups,
            projects=projects,
        )

    @staticmethod
    def get_python_version_info() -> str:
        return get_python_version_simple()
