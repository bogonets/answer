# -*- coding: utf-8 -*-

from functools import reduce
from recc.variables.http import URL_PATH_SEPARATOR
from recc.http import http_urls as u


def join_urls(*paths: str) -> str:
    assert paths

    def _join(x: str, y: str) -> str:
        if x[-1] == URL_PATH_SEPARATOR:
            if y[0] == URL_PATH_SEPARATOR:
                return x + y[1:]
            else:
                return x + y
        else:
            if y[0] == URL_PATH_SEPARATOR:
                return x + y
            else:
                return x + URL_PATH_SEPARATOR + y

    return reduce(_join, paths, u.root)


def v1_path(*paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v1, *paths)
    return path.format(**kwargs) if kwargs else path


def v2_path(*paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v2, *paths)
    return path.format(**kwargs) if kwargs else path


def v2_admin_path(*paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v2_admin, *paths)
    return path.format(**kwargs) if kwargs else path


def v2_dev_path(*paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v2_dev, *paths)
    return path.format(**kwargs) if kwargs else path


def v2_main_path(*paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v2_main, *paths)
    return path.format(**kwargs) if kwargs else path


def v2_public_path(*paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v2_public, *paths)
    return path.format(**kwargs) if kwargs else path


def v2_self_path(*paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v2_self, *paths)
    return path.format(**kwargs) if kwargs else path


def v2_plugins_path(*paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v2_plugins, *paths)
    return path.format(**kwargs) if kwargs else path


def v2_plugins_pplugin_path(plugin: str, *paths: str, **kwargs: str) -> str:
    path = join_urls(u.api_v2_plugins, u.pplugin.format(plugin=plugin), *paths)
    return path.format(**kwargs) if kwargs else path
