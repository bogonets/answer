# -*- coding: utf-8 -*-

from typing import Optional, Any
from multidict import CIMultiDictProxy


class HttpRequest:
    def __init__(
        self,
        *,
        method: Optional[str] = None,
        path: Optional[str] = None,
        data: Optional[Any] = None,
        headers: Optional[CIMultiDictProxy] = None,
    ):
        self.method = method
        self.path = path
        self.data = data
        self.headers = headers


class HttpResponse:
    def __init__(
        self,
        *,
        status: Optional[int] = None,
        reason: Optional[str] = None,
        data: Optional[Any] = None,
        headers: Optional[CIMultiDictProxy] = None,
    ):
        self.status = status
        self.reason = reason
        self.data = data
        self.headers = headers
