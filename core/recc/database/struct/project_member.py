# -*- coding: utf-8 -*-

from typing import Optional, Final
from recc.struct.structure_base import StructureBase
from recc.inspect.lexicographical_members import lexicographical_members


class ProjectMember(StructureBase):
    def __init__(
        self,
        project_uid: Optional[int] = None,
        user_uid: Optional[int] = None,
        permission_uid: Optional[int] = None,
    ):
        self.project_uid = project_uid
        self.user_uid = user_uid
        self.permission_uid = permission_uid


class ProjectMemberKeys:
    project_uid = "project_uid"
    user_uid = "user_uid"
    permission_uid = "permission_uid"


keys: Final[ProjectMemberKeys] = ProjectMemberKeys()
assert lexicographical_members(keys, ProjectMember())
