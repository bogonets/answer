# -*- coding: utf-8 -*-

from functools import reduce
from recc.variables.database import SQL_SEQUENCE_POINT


def _merge_query_lambda(prev_reduced: str, next_elem: str) -> str:
    stripped_next_elem = next_elem.strip()
    if stripped_next_elem:
        if stripped_next_elem[-1] == SQL_SEQUENCE_POINT:
            return prev_reduced + stripped_next_elem
        else:
            return prev_reduced + stripped_next_elem + SQL_SEQUENCE_POINT
    else:
        return prev_reduced


def merge_queries(*args: str) -> str:
    return reduce(_merge_query_lambda, args, str())
