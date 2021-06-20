# -*- coding: utf-8 -*-

from typing import List
from recc.session.session import Session
from recc.core.mixin.context_base import ContextBase
from recc.struct.project import Project


class ContextProject(ContextBase):
    async def create_project(
        self, session: Session, group_name: str, project_name: str
    ) -> None:
        user = await self.db.get_user_by_username(session.audience)
        group = await self.db.get_group_by_name(group_name)
        assert user.uid is not None
        assert group.uid is not None

        # TODO: test group_member

        maintainer_permission_uid = self.db.get_maintainer_permission_uid()
        await self.db.create_project(group.uid, project_name)
        project = await self.db.get_project_by_name(group.uid, project_name)
        assert project.uid is not None

        await self.db.create_project_member(
            project.uid, user.uid, maintainer_permission_uid
        )

    async def delete_global_project(
        self, session: Session, group_name: str, project_name: str
    ) -> None:
        user = await self.db.get_user_by_username(session.audience)
        group = await self.db.get_group_by_name(group_name)
        project = await self.db.get_project_by_name(group.uid, project_name)
        assert user.uid is not None
        assert group.uid is not None
        assert project.uid is not None

        # TODO: test permission

        await self.db.delete_project_by_uid(project.uid)

    async def get_projects(self, session: Session, group_name: str) -> List[Project]:
        user = await self.db.get_user_by_username(session.audience)
        group = await self.db.get_group_by_name(group_name)
        assert user.uid is not None
        assert group.uid is not None

        # TODO: test permission

        return await self.db.get_project_by_group_uid(group.uid)

    async def get_project(
        self, session: Session, group_name: str, project_name: str
    ) -> Project:
        user = await self.db.get_user_by_username(session.audience)
        group = await self.db.get_group_by_name(group_name)
        assert user.uid is not None
        assert group.uid is not None

        # TODO: test permission

        return await self.db.get_project_by_name(group.uid, project_name)
