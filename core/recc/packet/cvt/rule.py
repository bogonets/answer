# -*- coding: utf-8 -*-

from recc.database.struct.rule import Rule
from recc.packet.rule import RawRule, RuleA


def rule_to_raw(rule: Rule, is_admin: bool) -> RawRule:
    if is_admin:
        r_layout = True
        w_layout = True
        r_storage = True
        w_storage = True
        r_manager = True
        w_manager = True
        r_graph = True
        w_graph = True
        r_member = True
        w_member = True
        r_setting = True
        w_setting = True
    else:
        r_layout = rule.r_layout if rule.r_layout else False
        w_layout = rule.w_layout if rule.w_layout else False
        r_storage = rule.r_storage if rule.r_storage else False
        w_storage = rule.w_storage if rule.w_storage else False
        r_manager = rule.r_manager if rule.r_manager else False
        w_manager = rule.w_manager if rule.w_manager else False
        r_graph = rule.r_graph if rule.r_graph else False
        w_graph = rule.w_graph if rule.w_graph else False
        r_member = rule.r_member if rule.r_member else False
        w_member = rule.w_member if rule.w_member else False
        r_setting = rule.r_setting if rule.r_setting else False
        w_setting = rule.w_setting if rule.w_setting else False

    features = rule.features if rule.features else list()
    extra = rule.extra

    return RawRule(
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
        is_admin=is_admin,
        features=features,
        extra=extra,
    )


def rule_to_answer(rule: Rule) -> RuleA:
    slug = rule.slug if rule.slug else ""
    return RuleA(
        slug=slug,
        name=rule.name,
        description=rule.description,
        features=rule.features,
        extra=rule.extra,
        r_layout=rule.r_layout,
        w_layout=rule.w_layout,
        r_storage=rule.r_storage,
        w_storage=rule.w_storage,
        r_manager=rule.r_manager,
        w_manager=rule.w_manager,
        r_graph=rule.r_graph,
        w_graph=rule.w_graph,
        r_member=rule.r_member,
        w_member=rule.w_member,
        r_setting=rule.r_setting,
        w_setting=rule.w_setting,
        hidden=rule.hidden,
        lock=rule.lock,
        created_at=rule.created_at,
        updated_at=rule.updated_at,
    )
