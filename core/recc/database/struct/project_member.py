# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass


@dataclass
class ProjectMember:
    project_uid: Optional[int] = None
    user_uid: Optional[int] = None
    rule_uid: Optional[int] = None
