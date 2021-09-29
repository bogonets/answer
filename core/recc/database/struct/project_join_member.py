# -*- coding: utf-8 -*-

from dataclasses import dataclass
from recc.database.struct.project import Project
from recc.database.struct.project_member import ProjectMember


@dataclass
class ProjectJoinProjectMember(ProjectMember, Project):
    pass
