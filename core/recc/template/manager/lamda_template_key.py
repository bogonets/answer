# -*- coding: utf-8 -*-

from typing import Tuple
from recc.template.manager.lamda_template_position import LamdaTemplatePosition
from recc.variables.template import LAMBDA_TEMPLATE_KEY_DELIMITER


def make_template_key(
    position: LamdaTemplatePosition,
    category: str,
    name: str,
    delimiter=LAMBDA_TEMPLATE_KEY_DELIMITER,
) -> str:
    return position.name + delimiter + category + delimiter + name


class LamdaTemplateKey:

    position: LamdaTemplatePosition
    category: str
    name: str

    def __init__(
        self,
        position: LamdaTemplatePosition,
        category: str,
        name: str,
    ):
        self.position = position
        self.category = category
        self.name = name

    def to_tuple(self) -> Tuple[LamdaTemplatePosition, str, str]:
        return self.position, self.category, self.name

    def __str__(self) -> str:
        return make_template_key(self.position, self.category, self.name)

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
