# -*- coding: utf-8 -*-

from typing import Tuple, Union
from recc.rule.naming_base import valid_naming
from recc.template.manager.lamda_template_position import (
    LamdaTemplatePosition,
    LAMDA_TEMPLATE_POSITION_MAP,
)
from recc.rule.naming_template import (
    naming_lamda_template_key_name,
    split_lamda_template_key_name,
)


class LamdaTemplateKey:

    position: LamdaTemplatePosition
    category: str
    name: str

    def __init__(
        self,
        position: Union[LamdaTemplatePosition, str],
        category: str,
        name: str,
    ):
        if not valid_naming(category):
            raise ValueError(f"Invalid category: {category}")
        if not valid_naming(name):
            raise ValueError(f"Invalid name: {name}")

        if isinstance(position, LamdaTemplatePosition):
            self.position = position
        elif isinstance(position, str):
            self.position = LAMDA_TEMPLATE_POSITION_MAP[position]
        else:
            raise TypeError(f"Unsupported position type: {type(position).__name__}")

        self.category = category
        self.name = name

    def to_tuple(self) -> Tuple[LamdaTemplatePosition, str, str]:
        return self.position, self.category, self.name

    def to_fullpath(self) -> str:
        return naming_lamda_template_key_name(
            self.position.name, self.category, self.name
        )

    @classmethod
    def from_fullname(cls, fullname: str) -> "LamdaTemplateKey":
        position, category, name = split_lamda_template_key_name(fullname)
        return cls(position, category, name)

    def __str__(self) -> str:
        return self.to_fullpath()

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
