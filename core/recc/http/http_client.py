# -*- coding: utf-8 -*-

import requests
from time import time
from typing import Optional, Tuple
from recc.http.http_vars import (
    DEFAULT_SCHEME,
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    URL_ROOT,
    URL_API_VERSION,
    URL_API_HEARTBEAT,
)


def normalize_url_path(path: str) -> str:
    if not path:
        return URL_ROOT
    if path[0] != URL_ROOT:
        return URL_ROOT + path
    return path


def request(
    host: str,
    port: int,
    path=URL_ROOT,
    scheme=DEFAULT_SCHEME,
    timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
) -> Tuple[int, Optional[str]]:
    response = requests.get(
        f"{scheme}://{host}:{port}{normalize_url_path(path)}", timeout=timeout
    )
    code = response.status_code
    return code, response.text if code == 200 else str()


def request_heartbeat(
    host: str,
    port: int,
    scheme=DEFAULT_SCHEME,
    timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
) -> Tuple[int, Optional[str]]:
    return request(
        host=host, port=port, path=URL_API_HEARTBEAT, scheme=scheme, timeout=timeout
    )


def wait_heartbeat(
    host: str,
    port: int,
    scheme=DEFAULT_SCHEME,
    timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
) -> None:  # nocov
    begin = time()
    last_code = 0
    last_exception = None
    while time() - begin <= timeout:
        try:
            last_code, _ = request_heartbeat(
                host=host, port=port, scheme=scheme, timeout=timeout
            )
            if last_code == 200:
                return
        except Exception as e:  # noqa, nocov
            last_exception = e
    if last_exception:
        raise last_exception
    else:
        raise TimeoutError(
            f"Heartbeat timeout. (url={scheme}://{host}:{port},timeout={timeout}s,code={last_code})"  # noqa
        )


def request_version(
    host: str,
    port: int,
    scheme=DEFAULT_SCHEME,
    timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
) -> Tuple[int, Optional[str]]:
    return request(
        host=host, port=port, path=URL_API_VERSION, scheme=scheme, timeout=timeout
    )
