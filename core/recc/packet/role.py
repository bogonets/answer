# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class RoleA:
    slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateRoleQ:
    slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None

    def normalize_booleans(self) -> None:
        self.hidden = True if self.hidden else False
        self.lock = True if self.lock else False


@dataclass
class UpdateRoleQ:
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None
