# -*- coding: utf-8 -*-

from recc.database.struct.project import Project
from recc.packet.project import ProjectA


def project_to_answer(project: Project, group_slug: str) -> ProjectA:
    project_slug = project.slug if project.slug else ""
    return ProjectA(
        group_slug=group_slug,
        project_slug=project_slug,
        name=project.name,
        description=project.description,
        features=project.features,
        visibility=project.visibility,
        extra=project.extra,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )
