# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional

from recc.variables.database import VISIBILITY_LEVEL_PRIVATE


@dataclass
class Group:
    """It is mapped to the `group` table in the database."""

    uid: Optional[int] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    visibility: Optional[int] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class GroupA:
    slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    visibility: Optional[int] = None
    extra: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateGroupQ:
    slug: str
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
class UpdateGroupQ:
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    visibility: Optional[int] = None
    extra: Optional[Any] = None
