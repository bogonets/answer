# -*- coding: utf-8 -*-

from dataclasses import dataclass

from recc.packet.group import Group
from recc.packet.group_member import GroupMember
from recc.packet.project import Project


@dataclass
class GroupJoinGroupMember(GroupMember, Group):
    pass


@dataclass
class ProjectJoinGroupMember(GroupMember, Project):
    pass
