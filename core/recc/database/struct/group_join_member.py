# -*- coding: utf-8 -*-

from dataclasses import dataclass
from recc.database.struct.group import Group
from recc.database.struct.group_member import GroupMember
from recc.database.struct.project import Project


@dataclass
class GroupJoinGroupMember(GroupMember, Group):
    pass


@dataclass
class ProjectJoinGroupMember(GroupMember, Project):
    pass
