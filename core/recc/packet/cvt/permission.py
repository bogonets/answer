# -*- coding: utf-8 -*-

from recc.database.struct.permission import Permission
from recc.packet.permission import PermissionA


def permission_to_answer(permission: Permission) -> PermissionA:
    return PermissionA(
        slug=permission.slug,
        description=permission.description,
        extra=permission.extra,
        created_at=permission.created_at,
    )
