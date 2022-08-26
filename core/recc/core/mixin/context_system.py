# -*- coding: utf-8 -*-

from recc.chrono.datetime import tznow
from recc.core.mixin.context_base import ContextBase
from recc.packet.system import SystemOverviewA
from recc.util.python_version import get_python_version_simple


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
        return get_python_version_simple()
