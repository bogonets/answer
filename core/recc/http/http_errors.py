# -*- coding: utf-8 -*-

from aiohttp.web_exceptions import HTTPClientError, HTTPServerError

HTTP_RECC_CLIENT_STATUS_CODE_BEGIN = 460
HTTP_RECC_SERVER_STATUS_CODE_BEGIN = 560


def client_status_code(offset: int) -> int:
    return HTTP_RECC_CLIENT_STATUS_CODE_BEGIN + offset


def server_status_code(offset: int) -> int:
    return HTTP_RECC_SERVER_STATUS_CODE_BEGIN + offset


######################
# CLIENT ERROR (4xx) #
######################


class HTTPReccClientError(HTTPClientError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert HTTP_RECC_CLIENT_STATUS_CODE_BEGIN <= self.status_code < 500


class HTTPReccUnknownClientError(HTTPReccClientError):
    status_code = client_status_code(0)

    def __init__(self, reason="Unknown recc client error"):
        super().__init__(reason=reason)


class HTTPReccAccessTokenError(HTTPReccClientError):
    status_code = client_status_code(1)

    def __init__(self, reason="Access token error"):
        super().__init__(reason=reason)


class HTTPReccRefreshTokenError(HTTPReccClientError):
    status_code = client_status_code(2)

    def __init__(self, reason="Refresh token error"):
        super().__init__(reason=reason)


######################
# SERVER ERROR (5xx) #
######################


class HTTPReccServerError(HTTPServerError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert HTTP_RECC_SERVER_STATUS_CODE_BEGIN <= self.status_code < 600


class HTTPReccUnknownServerError(HTTPReccServerError):
    status_code = server_status_code(0)

    def __init__(self, reason="Unknown recc server error"):
        super().__init__(reason=reason)


class HTTPReccUninitializedService(HTTPReccServerError):
    status_code = server_status_code(1)

    def __init__(self, reason="Uninitialized service"):
        super().__init__(reason=reason)
