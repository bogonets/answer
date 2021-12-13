# -*- coding: utf-8 -*-

from typing import Optional, Any, List
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class RawRole:
    r_layout: bool = False
    w_layout: bool = False
    r_storage: bool = False
    w_storage: bool = False
    r_manager: bool = False
    w_manager: bool = False
    r_graph: bool = False
    w_graph: bool = False
    r_member: bool = False
    w_member: bool = False
    r_setting: bool = False
    w_setting: bool = False
    is_admin: bool = False
    features: List[str] = field(default_factory=list)
    extra: Any = None

    @classmethod
    def all(cls, x: bool, features: Optional[List[str]] = None, extra: Any = None):
        f = features if features else list()
        return cls(x, x, x, x, x, x, x, x, x, x, x, x, x, f, extra)

    @classmethod
    def all_true(cls, features: Optional[List[str]] = None, extra: Any = None):
        return cls.all(True, features, extra)

    @classmethod
    def all_false(cls, features: Optional[List[str]] = None, extra: Any = None):
        return cls.all(False, features, extra)


@dataclass
class RoleA:
    slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    extra: Optional[Any] = None
    r_layout: Optional[bool] = None
    w_layout: Optional[bool] = None
    r_storage: Optional[bool] = None
    w_storage: Optional[bool] = None
    r_manager: Optional[bool] = None
    w_manager: Optional[bool] = None
    r_graph: Optional[bool] = None
    w_graph: Optional[bool] = None
    r_member: Optional[bool] = None
    w_member: Optional[bool] = None
    r_setting: Optional[bool] = None
    w_setting: Optional[bool] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateRoleQ:
    slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    extra: Optional[Any] = None
    r_layout: Optional[bool] = None
    w_layout: Optional[bool] = None
    r_storage: Optional[bool] = None
    w_storage: Optional[bool] = None
    r_manager: Optional[bool] = None
    w_manager: Optional[bool] = None
    r_graph: Optional[bool] = None
    w_graph: Optional[bool] = None
    r_member: Optional[bool] = None
    w_member: Optional[bool] = None
    r_setting: Optional[bool] = None
    w_setting: Optional[bool] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None

    def normalize_booleans(self) -> None:
        self.r_layout = True if self.r_layout else False
        self.w_layout = True if self.w_layout else False
        self.r_storage = True if self.r_storage else False
        self.w_storage = True if self.w_storage else False
        self.r_manager = True if self.r_manager else False
        self.w_manager = True if self.w_manager else False
        self.r_graph = True if self.r_graph else False
        self.w_graph = True if self.w_graph else False
        self.r_member = True if self.r_member else False
        self.w_member = True if self.w_member else False
        self.r_setting = True if self.r_setting else False
        self.w_setting = True if self.w_setting else False
        self.hidden = True if self.hidden else False
        self.lock = True if self.lock else False


@dataclass
class UpdateRoleQ:
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    extra: Optional[Any] = None
    r_layout: Optional[bool] = None
    w_layout: Optional[bool] = None
    r_storage: Optional[bool] = None
    w_storage: Optional[bool] = None
    r_manager: Optional[bool] = None
    w_manager: Optional[bool] = None
    r_graph: Optional[bool] = None
    w_graph: Optional[bool] = None
    r_member: Optional[bool] = None
    w_member: Optional[bool] = None
    r_setting: Optional[bool] = None
    w_setting: Optional[bool] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None
