# -*- coding: utf-8 -*-

from aiohttp.web_exceptions import HTTPServerError


class HTTPReccError(HTTPServerError):
    """The status code is greater than or equal to 520."""

    pass


class HTTPReccUnknownError(HTTPReccError):
    status_code = 520

    def __init__(self, reason="Unknown recc error"):
        super().__init__(reason=reason)
