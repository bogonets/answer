# -*- coding: utf-8 -*-

from sys import version_info

from recc.chrono.datetime import tznow
from recc.core.mixin.context_base import ContextBase
from recc.packet.system import SystemOverviewA


class ContextSystem(ContextBase):
    async def get_system_overview(self) -> SystemOverviewA:
        time = tznow()
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
        return f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
