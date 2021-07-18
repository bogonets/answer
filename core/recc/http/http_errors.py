# -*- coding: utf-8 -*-

from aiohttp.web_exceptions import HTTPServerError


class HTTPReccError(HTTPServerError):
    """The status code is greater than or equal to 520."""
    pass


class HTTPReccNotInitializedError(HTTPReccError):
    status_code = 520

    def __init__(self):
        super().__init__(reason="Not initialized")


class HTTPReccAlreadyInitializedError(HTTPReccError):
    status_code = 521

    def __init__(self):
        super().__init__(reason="Already initialized")
