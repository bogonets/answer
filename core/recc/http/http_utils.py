# -*- coding: utf-8 -*-

from functools import reduce
from typing import Any, Mapping, Optional
from urllib.parse import urlencode

from recc.http import http_path_keys as p
from recc.http import http_urls as u
from recc.variables.http import URI_PATH_SEPARATOR, URI_QUERY_PREFIX


def strip_prefix_slash(path: str) -> str:
    assert len(u.root) == 1
    assert path
    return path[1:] if path[0] == u.root else path


def join_urls(*paths: str) -> str:
    assert paths

    def _join(x: str, y: str) -> str:
        if x[-1] == URI_PATH_SEPARATOR:
            if y[0] == URI_PATH_SEPARATOR:
                return x + y[1:]
            else:
                return x + y
        else:
            if y[0] == URI_PATH_SEPARATOR:
                return x + y
            else:
                return x + URI_PATH_SEPARATOR + y

    return reduce(_join, paths, u.root)


def join_urls_and_query_map(
    *paths: str,
    query: Optional[Mapping[str, Any]] = None,
) -> str:
    if query:
        return join_urls(*paths) + URI_QUERY_PREFIX + urlencode(query)
    else:
        return join_urls(*paths)


def join_urls_and_queries(*paths: str, **queries: str) -> str:
    return join_urls_and_query_map(*paths, query=queries)


def v1_path(*paths: str, query: Optional[Mapping[str, Any]] = None) -> str:
    return join_urls_and_query_map(u.api_v1, *paths, query=query)


def v2_path(*paths: str, query: Optional[Mapping[str, Any]] = None) -> str:
    return join_urls_and_query_map(u.api_v2, *paths, query=query)


def v2_admin_path(path: str, query: Optional[Mapping[str, Any]] = None) -> str:
    return join_urls_and_query_map(u.api_v2_admin, path, query=query)


def v2_dev_path(path: str, query: Optional[Mapping[str, Any]] = None) -> str:
    return join_urls_and_query_map(u.api_v2_dev, path, query=query)


def v2_main_path(path: str, query: Optional[Mapping[str, Any]] = None) -> str:
    return join_urls_and_query_map(u.api_v2_main, path, query=query)


def v2_public_path(path: str, query: Optional[Mapping[str, Any]] = None) -> str:
    return join_urls_and_query_map(u.api_v2_public, path, query=query)


def v2_self_path(path: str, query: Optional[Mapping[str, Any]] = None) -> str:
    return join_urls_and_query_map(u.api_v2_self, path, query=query)


def v2_plugins_path(path: str, query: Optional[Mapping[str, Any]] = None) -> str:
    return join_urls_and_query_map(u.api_v2_plugins, path, query=query)


def v2_plugins_pplugin_path(
    plugin: str,
    path: str,
    query: Optional[Mapping[str, Any]] = None,
) -> str:
    return join_urls_and_query_map(
        u.api_v2_plugins,
        u.pplugin.format_map({p.plugin: plugin}),
        path,
        query=query,
    )
