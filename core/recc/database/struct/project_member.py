# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional


@dataclass
class ProjectMember:
    project_uid: Optional[int] = None
    user_uid: Optional[int] = None
    role_uid: Optional[int] = None
