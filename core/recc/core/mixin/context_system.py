# -*- coding: utf-8 -*-

from recc.core.mixin.context_base import ContextBase
from recc.core.struct.system_overview import SystemOverview


class ContextSystem(ContextBase):
    async def get_system_overview(self) -> SystemOverview:
        users = await self.database.get_users_count()
        groups = await self.database.get_groups_count()
        projects = await self.database.get_projects_count()
        return SystemOverview(users, groups, projects)
