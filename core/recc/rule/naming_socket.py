# -*- coding: utf-8 -*-

from recc.rule.naming_base import merge_naming
from recc.variables.naming import NAME_DELIMITER, PREFIX_RECC, SUFFIX_SOCKET


def naming_socket(task_name: str, hidden=False) -> str:
    result = merge_naming(
        PREFIX_RECC,
        task_name,
        SUFFIX_SOCKET,
        delimiter=NAME_DELIMITER,
    )
    if hidden:
        return "." + result
    else:
        return result
