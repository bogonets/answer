# -*- coding: utf-8 -*-

from typing import List, Optional, Any, Union
from recc.core.mixin.context_base import ContextBase
from recc.database.struct.rule import Rule
from recc.packet.rule import RawRule
from recc.packet.cvt.rule import rule_to_raw
from recc.session.session_ex import SessionEx


class ContextRule(ContextBase):
    async def create_rule(
        self,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout=False,
        w_layout=False,
        r_storage=False,
        w_storage=False,
        r_manager=False,
        w_manager=False,
        r_graph=False,
        w_graph=False,
        r_member=False,
        w_member=False,
        r_setting=False,
        w_setting=False,
        hidden=False,
        lock=False,
    ) -> int:
        rule_uid = await self.database.insert_rule(
            slug=slug,
            name=name,
            description=description,
            features=features,
            extra=extra,
            r_layout=r_layout,
            w_layout=w_layout,
            r_storage=r_storage,
            w_storage=w_storage,
            r_manager=r_manager,
            w_manager=w_manager,
            r_graph=r_graph,
            w_graph=w_graph,
            r_member=r_member,
            w_member=w_member,
            r_setting=r_setting,
            w_setting=w_setting,
            hidden=hidden,
            lock=lock,
        )
        await self.cache.set_rule(slug, rule_uid)
        return rule_uid

    @staticmethod
    def _is_rule_equals_for_update(
        rule: Rule,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout: Optional[bool] = None,
        w_layout: Optional[bool] = None,
        r_storage: Optional[bool] = None,
        w_storage: Optional[bool] = None,
        r_manager: Optional[bool] = None,
        w_manager: Optional[bool] = None,
        r_graph: Optional[bool] = None,
        w_graph: Optional[bool] = None,
        r_member: Optional[bool] = None,
        w_member: Optional[bool] = None,
        r_setting: Optional[bool] = None,
        w_setting: Optional[bool] = None,
        hidden: Optional[bool] = None,
    ) -> bool:
        """
        When rule is 'locked', all attributes except `lock` must not be changed.
        """

        if slug is not None:
            if rule.slug != slug:
                return False
        if name is not None:
            if rule.name != name:
                return False
        if description is not None:
            if rule.description != description:
                return False
        if features is not None:
            if rule.features != features:
                return False
        if extra is not None:
            if rule.extra != extra:
                return False
        if r_layout is not None:
            if rule.r_layout != r_layout:
                return False
        if w_layout is not None:
            if rule.w_layout != w_layout:
                return False
        if r_storage is not None:
            if rule.r_storage != r_storage:
                return False
        if w_storage is not None:
            if rule.w_storage != w_storage:
                return False
        if r_manager is not None:
            if rule.r_manager != r_manager:
                return False
        if w_manager is not None:
            if rule.w_manager != w_manager:
                return False
        if r_graph is not None:
            if rule.r_graph != r_graph:
                return False
        if w_graph is not None:
            if rule.w_graph != w_graph:
                return False
        if r_member is not None:
            if rule.r_member != r_member:
                return False
        if w_member is not None:
            if rule.w_member != w_member:
                return False
        if r_setting is not None:
            if rule.r_setting != r_setting:
                return False
        if w_setting is not None:
            if rule.w_setting != w_setting:
                return False
        if hidden is not None:
            if rule.hidden != hidden:
                return False
        return True

    async def update_rule(
        self,
        uid: int,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        features: Optional[List[str]] = None,
        extra: Optional[Any] = None,
        r_layout: Optional[bool] = None,
        w_layout: Optional[bool] = None,
        r_storage: Optional[bool] = None,
        w_storage: Optional[bool] = None,
        r_manager: Optional[bool] = None,
        w_manager: Optional[bool] = None,
        r_graph: Optional[bool] = None,
        w_graph: Optional[bool] = None,
        r_member: Optional[bool] = None,
        w_member: Optional[bool] = None,
        r_setting: Optional[bool] = None,
        w_setting: Optional[bool] = None,
        hidden: Optional[bool] = None,
        lock: Optional[bool] = None,
        force=False,
    ) -> None:
        if not force:
            rule = await self.database.select_rule_by_uid(uid)
            if rule.lock:
                rule_equals = self._is_rule_equals_for_update(
                    rule,
                    slug,
                    name,
                    description,
                    features,
                    extra,
                    r_layout,
                    w_layout,
                    r_storage,
                    w_storage,
                    r_manager,
                    w_manager,
                    r_graph,
                    w_graph,
                    r_member,
                    w_member,
                    r_setting,
                    w_setting,
                    hidden,
                )
                if not rule_equals:
                    raise RuntimeError(f"Locked rule: {uid}")

        await self.database.update_rule_by_uid(
            uid=uid,
            slug=slug,
            name=name,
            description=description,
            features=features,
            extra=extra,
            r_layout=r_layout,
            w_layout=w_layout,
            r_storage=r_storage,
            w_storage=w_storage,
            r_manager=r_manager,
            w_manager=w_manager,
            r_graph=r_graph,
            w_graph=w_graph,
            r_member=r_member,
            w_member=w_member,
            r_setting=r_setting,
            w_setting=w_setting,
            hidden=hidden,
            lock=lock,
        )
        if slug is not None:
            await self.cache.remove_rule_by_uid(uid)
            await self.cache.set_rule(slug, uid)

    async def delete_rule(self, uid: int, force=False) -> None:
        if not force:
            if await self.database.select_rule_lock_by_uid(uid):
                raise RuntimeError(f"Locked rule: {uid}")
        await self.database.delete_rule_by_uid(uid)
        await self.cache.remove_rule_by_uid(uid)

    async def get_rule(self, uid: int) -> Rule:
        return await self.database.select_rule_by_uid(uid)

    async def get_rules(self) -> List[Rule]:
        return await self.database.select_rule_all()

    async def get_group_rule(self, user_uid: int, group_uid: int) -> Rule:
        return await self.database.select_rule_by_user_uid_and_group_uid(
            user_uid, group_uid
        )

    async def get_project_rule(self, user_uid: int, project_uid: int) -> Rule:
        return await self.database.select_rule_by_user_uid_and_project_uid(
            user_uid, project_uid
        )

    async def get_best_rule(
        self, user_uid: int, group_uid: int, project_uid: int
    ) -> Rule:
        try:
            return await self.get_project_rule(user_uid, project_uid)
        except:  # noqa
            return await self.get_group_rule(user_uid, group_uid)

    async def get_group_raw_rule(
        self, session: SessionEx, group: Union[str, int]
    ) -> RawRule:
        try:
            if isinstance(group, int):
                group_uid = group
            elif isinstance(group, str):
                group_uid = await self.get_group_uid(group)
            else:
                group_uid = await self.get_group_uid(str(group))

            rule = await self.get_group_rule(session.uid, group_uid)
            return rule_to_raw(rule, session.is_admin)
        except:  # noqa
            if session.is_admin:
                return RawRule.all_true()
            else:
                return RawRule.all_false()

    async def get_project_raw_rule(
        self, session: SessionEx, group: Union[str, int], project: Union[str, int]
    ) -> RawRule:
        try:
            if isinstance(group, int):
                group_uid = group
            elif isinstance(group, str):
                group_uid = await self.get_group_uid(group)
            else:
                group_uid = await self.get_group_uid(str(group))

            if isinstance(project, int):
                project_uid = project
            elif isinstance(project, str):
                project_uid = await self.get_project_uid(group_uid, project)
            else:
                project_uid = await self.get_project_uid(group_uid, str(project))

            rule = await self.get_best_rule(session.uid, group_uid, project_uid)
            return rule_to_raw(rule, session.is_admin)
        except:  # noqa
            if session.is_admin:
                return RawRule.all_true()
            else:
                return RawRule.all_false()
