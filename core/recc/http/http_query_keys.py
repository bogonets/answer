# -*- coding: utf-8 -*-

from io import StringIO

k_op = "op"
v_op_range = "range"


def query_builder(**kwargs) -> str:
    if len(kwargs) == 0:
        return ""

    q = StringIO()
    fk, fv = kwargs.popitem()
    q.write(f"?{fk}={fv}")

    for k, v in kwargs.items():
        q.write(f"&{k}={v}")

    return q.getvalue()
