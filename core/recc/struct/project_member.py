# -*- coding: utf-8 -*-

from typing import Optional
from recc.struct._structure import _Structure


class ProjectMember(_Structure):
    def __init__(
        self,
        project_uid: Optional[int] = None,
        user_uid: Optional[int] = None,
        permission_uid: Optional[int] = None,
        **kwargs,
    ):
        self.project_uid = project_uid
        self.user_uid = user_uid
        self.permission_uid = permission_uid
        self.kwargs = kwargs
