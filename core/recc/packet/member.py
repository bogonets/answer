# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class MemberA:
    username: str
    role: str


@dataclass
class CreateMemberQ:
    username: str
    role: str


@dataclass
class UpdateMemberQ:
    username: str
    role: str
