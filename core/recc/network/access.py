# -*- coding: utf-8 -*-

from typing import Optional
from requests import get
from http import HTTPStatus


def accessible_network(
    address: str,
    timeout: Optional[float] = None,
) -> bool:
    try:
        return get(address, timeout=timeout).status_code == HTTPStatus.OK
    except BaseException:  # noqa
        return False
