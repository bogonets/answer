# -*- coding: utf-8 -*-

from recc.database.struct.role import Role
from recc.packet.role import RawRole, RoleA


def role_to_raw(role: Role, is_admin: bool) -> RawRole:
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
        r_layout = role.r_layout if role.r_layout else False
        w_layout = role.w_layout if role.w_layout else False
        r_storage = role.r_storage if role.r_storage else False
        w_storage = role.w_storage if role.w_storage else False
        r_manager = role.r_manager if role.r_manager else False
        w_manager = role.w_manager if role.w_manager else False
        r_graph = role.r_graph if role.r_graph else False
        w_graph = role.w_graph if role.w_graph else False
        r_member = role.r_member if role.r_member else False
        w_member = role.w_member if role.w_member else False
        r_setting = role.r_setting if role.r_setting else False
        w_setting = role.w_setting if role.w_setting else False

    features = role.features if role.features else list()
    extra = role.extra

    return RawRole(
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


def role_to_answer(role: Role) -> RoleA:
    slug = role.slug if role.slug else ""
    return RoleA(
        slug=slug,
        name=role.name,
        description=role.description,
        features=role.features,
        extra=role.extra,
        r_layout=role.r_layout,
        w_layout=role.w_layout,
        r_storage=role.r_storage,
        w_storage=role.w_storage,
        r_manager=role.r_manager,
        w_manager=role.w_manager,
        r_graph=role.r_graph,
        w_graph=role.w_graph,
        r_member=role.r_member,
        w_member=role.w_member,
        r_setting=role.r_setting,
        w_setting=role.w_setting,
        hidden=role.hidden,
        lock=role.lock,
        created_at=role.created_at,
        updated_at=role.updated_at,
    )
