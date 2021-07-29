# -*- coding: utf-8 -*-

from typing import Optional, Final
from recc.struct.structure_base import StructureBase
from recc.algorithm.lexicographical import lexicographical_equals


class GroupMember(StructureBase):
    def __init__(
        self,
        group_uid: Optional[int] = None,
        user_uid: Optional[int] = None,
        permission_uid: Optional[int] = None,
    ):
        self.group_uid = group_uid
        self.user_uid = user_uid
        self.permission_uid = permission_uid


class GroupMemberKeys:
    group_uid = "group_uid"
    user_uid = "user_uid"
    permission_uid = "permission_uid"


keys: Final[GroupMemberKeys] = GroupMemberKeys()
assert lexicographical_equals(keys, GroupMember())
