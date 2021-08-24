# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class MemberA:
    username: str
    permission: str


@dataclass
class CreateMemberQ:
    username: str
    permission: str


@dataclass
class UpdateMemberQ:
    username: str
    permission: str
