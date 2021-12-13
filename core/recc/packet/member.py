# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class MemberA:
    username: str
    rule: str


@dataclass
class CreateMemberQ:
    username: str
    rule: str


@dataclass
class UpdateMemberQ:
    username: str
    rule: str
