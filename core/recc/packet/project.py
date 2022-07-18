# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional

from recc.variables.database import VISIBILITY_LEVEL_PRIVATE


@dataclass
class Project:
    """It is mapped to the `project` table in the database."""

    uid: Optional[int] = None
    group_uid: Optional[int] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    visibility: Optional[int] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class ProjectA:
    group_slug: str
    project_slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    visibility: Optional[int] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateProjectQ:
    group_slug: str
    project_slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    visibility: Optional[int] = None
    extra: Optional[Any] = None

    def get_visibility(self) -> int:
        if self.visibility is not None:
            return self.visibility
        return VISIBILITY_LEVEL_PRIVATE


@dataclass
class UpdateProjectQ:
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    visibility: Optional[int] = None
    extra: Optional[Any] = None


@dataclass
class ProjectOverviewA:
    layouts: Optional[int] = None
    tables: Optional[int] = None
    tasks: Optional[int] = None
    members: Optional[int] = None
