# -*- coding: utf-8 -*-

from enum import Enum
from recc.enumerate.string_to_enum import string_to_enum_map


class LamdaTemplatePosition(Enum):
    Builtin = 0
    Package = 1
    Storage = 2


LAMDA_TEMPLATE_POSITION_MAP = string_to_enum_map(LamdaTemplatePosition)
