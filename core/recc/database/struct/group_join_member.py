# -*- coding: utf-8 -*-

from dataclasses import dataclass
from recc.database.struct.group import Group
from recc.database.struct.group_member import GroupMember


@dataclass
class GroupJoinMember(GroupMember, Group):
    pass
