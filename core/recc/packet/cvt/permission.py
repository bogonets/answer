# -*- coding: utf-8 -*-

from recc.database.struct.permission import Permission
from recc.packet.permission import PermissionA


def permission_to_answer(permission: Permission) -> PermissionA:
    name = permission.name if permission.name else ""
    return PermissionA(
        name=name,
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
        created_at=permission.created_at,
        updated_at=permission.updated_at,
    )
