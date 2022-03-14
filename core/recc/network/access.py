# -*- coding: utf-8 -*-

from typing import Optional
from recc.http.http_client import HttpClient


async def accessible_network(
    address: str,
    timeout: Optional[float] = None,
) -> bool:
    try:
        client = HttpClient(address, timeout=timeout)
        await client.get()
        return True
    except BaseException:  # noqa
        return False
