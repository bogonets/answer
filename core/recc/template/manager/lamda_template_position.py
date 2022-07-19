# -*- coding: utf-8 -*-

from enum import Enum


class LamdaTemplatePosition(Enum):
    Builtin = 0
    Package = 1
    Storage = 2


LAMDA_TEMPLATE_POSITION_MAP = {
    "Builtin": LamdaTemplatePosition.Builtin,
    "Package": LamdaTemplatePosition.Package,
    "Storage": LamdaTemplatePosition.Storage,
}
LAMDA_TEMPLATE_POSITION_NAME_MAP = {
    v: k for k, v in LAMDA_TEMPLATE_POSITION_MAP.items()
}
