# -*- coding: utf-8 -*-

from typing import Optional, Final
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


@dataclass
class ProjectMember:
    project_uid: Optional[int] = None
    user_uid: Optional[int] = None
    permission_uid: Optional[int] = None


class ProjectMemberKeys:
    project_uid = "project_uid"
    user_uid = "user_uid"
    permission_uid = "permission_uid"


keys: Final[ProjectMemberKeys] = ProjectMemberKeys()
assert lexicographical_members(keys, ProjectMember())
