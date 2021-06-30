# -*- coding: utf-8 -*-

from typing import List, Optional, Any
from recc.session.session import Session
from recc.core.mixin.context_base import ContextBase
from recc.struct.layout import Layout


class ContextLayout(ContextBase):
    async def create_layout(
        self,
        _: Session,
        project_name: str,
        layout_name: str,
        extra: Optional[Any] = None,
    ) -> None:
        anonymous_group_uid = self.database.get_anonymous_group_uid()
        project = await self.database.get_project_by_name(
            anonymous_group_uid, project_name
        )
        assert project.uid is not None
        await self.database.create_layout(project.uid, layout_name)
        if extra is not None:
            await self.database.update_layout_extra_by_name(
                project.uid, layout_name, extra
            )

    async def get_layouts(self, _: Session, project_name: str) -> List[Layout]:
        anonymous_group_uid = self.database.get_anonymous_group_uid()
        project = await self.database.get_project_by_name(
            anonymous_group_uid, project_name
        )
        assert project.uid is not None
        return await self.database.get_layout_by_project_uid(project.uid)

    async def get_layout(
        self, _: Session, project_name: str, layout_name: str
    ) -> Layout:
        anonymous_group_uid = self.database.get_anonymous_group_uid()
        project = await self.database.get_project_by_name(
            anonymous_group_uid, project_name
        )
        assert project.uid is not None
        return await self.database.get_layout_by_name(project.uid, layout_name)

    async def exists_layout(
        self, session: Session, project_name: str, layout_name: str
    ) -> bool:
        try:
            await self.get_layout(session, project_name, layout_name)
            return True
        except:  # noqa
            return False

    async def set_layout_extra(
        self, _: Session, project_name: str, layout_name: str, extra: Any
    ) -> None:
        anonymous_group_uid = self.database.get_anonymous_group_uid()
        project = await self.database.get_project_by_name(
            anonymous_group_uid, project_name
        )
        assert project.uid is not None
        await self.database.update_layout_extra_by_name(project.uid, layout_name, extra)

    async def remove_layout(
        self, _: Session, project_name: str, layout_name: str
    ) -> None:
        anonymous_group_uid = self.database.get_anonymous_group_uid()
        project = await self.database.get_project_by_name(
            anonymous_group_uid, project_name
        )
        assert project.uid is not None
        await self.database.delete_layout_by_name(project.uid, layout_name)
