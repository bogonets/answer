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


def v1_path(*paths) -> str:
    return join_urls(u.api_v1, *paths)


def v2_path(*paths) -> str:
    return join_urls(u.api_v2, *paths)


def v2_public_path(*paths) -> str:
    return join_urls(u.api_v2_public, *paths)
