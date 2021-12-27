# -*- coding: utf-8 -*-

from recc.database.struct.role import Role
from recc.packet.role import RoleA


def role_to_answer(role: Role) -> RoleA:
    slug = role.slug if role.slug else ""
    return RoleA(
        slug=slug,
        name=role.name,
        description=role.description,
        extra=role.extra,
        hidden=role.hidden,
        lock=role.lock,
        created_at=role.created_at,
        updated_at=role.updated_at,
    )
