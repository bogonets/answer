# -*- coding: utf-8 -*-

from recc.database.struct.rule import Rule
from recc.packet.permission import RawPermission, PermissionA


def permission_to_raw(permission: Rule, is_admin: bool) -> RawPermission:
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
        r_layout = permission.r_layout if permission.r_layout else False
        w_layout = permission.w_layout if permission.w_layout else False
        r_storage = permission.r_storage if permission.r_storage else False
        w_storage = permission.w_storage if permission.w_storage else False
        r_manager = permission.r_manager if permission.r_manager else False
        w_manager = permission.w_manager if permission.w_manager else False
        r_graph = permission.r_graph if permission.r_graph else False
        w_graph = permission.w_graph if permission.w_graph else False
        r_member = permission.r_member if permission.r_member else False
        w_member = permission.w_member if permission.w_member else False
        r_setting = permission.r_setting if permission.r_setting else False
        w_setting = permission.w_setting if permission.w_setting else False

    features = permission.features if permission.features else list()
    extra = permission.extra

    return RawPermission(
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


def permission_to_answer(permission: Rule) -> PermissionA:
    slug = permission.slug if permission.slug else ""
    return PermissionA(
        slug=slug,
        name=permission.name,
        description=permission.description,
        features=permission.features,
        extra=permission.extra,
        r_layout=permission.r_layout,
        w_layout=permission.w_layout,
        r_storage=permission.r_storage,
        w_storage=permission.w_storage,
        r_manager=permission.r_manager,
        w_manager=permission.w_manager,
        r_graph=permission.r_graph,
        w_graph=permission.w_graph,
        r_member=permission.r_member,
        w_member=permission.w_member,
        r_setting=permission.r_setting,
        w_setting=permission.w_setting,
        hidden=permission.hidden,
        lock=permission.lock,
        created_at=permission.created_at,
        updated_at=permission.updated_at,
    )
