# -*- coding: utf-8 -*-

from typing import Tuple
from recc.rule.naming_base import merge_naming, split_naming
from recc.variables.template import LAMDA_TEMPLATE_KEY_DELIMITER


def naming_lamda_template_key_name(position: str, category: str, name: str) -> str:
    return merge_naming(
        position,
        category,
        name,
        delimiter=LAMDA_TEMPLATE_KEY_DELIMITER,
    )


def split_lamda_template_key_name(fullname: str) -> Tuple[str, str, str]:
    names = split_naming(fullname, delimiter=LAMDA_TEMPLATE_KEY_DELIMITER)
    assert len(names) == 3, "The lamda-template-key-name requires 3 fields."
    return names[0], names[1], names[2]
