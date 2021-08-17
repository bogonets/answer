# -*- coding: utf-8 -*-

from recc.core.mixin.context_base import ContextBase
from recc.packet.system import SystemOverviewA


class ContextSystem(ContextBase):
    async def get_system_overview(self) -> SystemOverviewA:
        users = await self.database.get_users_count()
        groups = await self.database.get_groups_count()
        projects = await self.database.get_projects_count()
        return SystemOverviewA(users, groups, projects)
