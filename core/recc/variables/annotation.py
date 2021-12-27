# -*- coding: utf-8 -*-

from enum import Enum

ANNOTATION_PERMISSIONS = "__recc_permissions__"
ANNOTATION_DOMAIN = "__recc_domain__"


class Domain(Enum):
    Unknown = 0
    Group = 1
    Project = 2
