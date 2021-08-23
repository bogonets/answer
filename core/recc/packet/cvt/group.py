# -*- coding: utf-8 -*-

from recc.packet.group import GroupA
from recc.database.struct.group import Group


def group_to_answer(group: Group) -> GroupA:
    group_slug = group.slug if group.slug else ""
    return GroupA(
        slug=group_slug,
        name=group.name,
        description=group.description,
        features=group.features,
        visibility=group.visibility,
        extra=group.extra,
        created_at=group.created_at,
        updated_at=group.updated_at,
    )
