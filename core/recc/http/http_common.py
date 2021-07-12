# -*- coding: utf-8 -*-

from functools import reduce
from recc.http.http_vars import URL_PATH_SEPARATOR
from recc.http import http_urls as u


def join_urls(*paths) -> str:
    assert paths

    def _join(x: str, y: str) -> str:
        if y[0] == URL_PATH_SEPARATOR:
            return x + y
        else:
            return y + URL_PATH_SEPARATOR + y

    return reduce(_join, paths, u.root)
