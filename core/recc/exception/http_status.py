# -*- coding: utf-8 -*-

from http import HTTPStatus
from recc.exception.base_exception import ReccBaseException

# HTTP Status codes
# - https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# - https://developer.mozilla.org/ko/docs/Web/HTTP/Status

# ----------------------
# Informational response
# ----------------------

CODE_INFORMATIONAL_RESPONSE = 100
CODE_CONTINUE = HTTPStatus.CONTINUE
CODE_SWITCHING_PROTOCOLS = HTTPStatus.SWITCHING_PROTOCOLS
CODE_PROCESSING = HTTPStatus.PROCESSING

# ----------
# Successful
# ----------

CODE_SUCCESSFUL = 200
CODE_OK = HTTPStatus.OK
CODE_CREATED = HTTPStatus.CREATED
CODE_ACCEPTED = HTTPStatus.ACCEPTED
CODE_NON_AUTHORITATIVE_INFORMATION = HTTPStatus.NON_AUTHORITATIVE_INFORMATION
CODE_NO_CONTENT = HTTPStatus.NO_CONTENT
CODE_RESET_CONTENT = HTTPStatus.RESET_CONTENT
CODE_PARTIAL_CONTENT = HTTPStatus.PARTIAL_CONTENT
CODE_MULTI_STATUS = HTTPStatus.MULTI_STATUS
CODE_ALREADY_REPORTED = HTTPStatus.ALREADY_REPORTED
CODE_IM_USED = HTTPStatus.IM_USED

# -----------
# Redirection
# -----------

CODE_REDIRECTION = 300
CODE_MULTIPLE_CHOICES = HTTPStatus.MULTIPLE_CHOICES
CODE_MOVED_PERMANENTLY = HTTPStatus.MOVED_PERMANENTLY
CODE_FOUND = HTTPStatus.FOUND
CODE_SEE_OTHER = HTTPStatus.SEE_OTHER
CODE_NOT_MODIFIED = HTTPStatus.NOT_MODIFIED
CODE_USE_PROXY = HTTPStatus.USE_PROXY
CODE_TEMPORARY_REDIRECT = HTTPStatus.TEMPORARY_REDIRECT
CODE_PERMANENT_REDIRECT = HTTPStatus.PERMANENT_REDIRECT

# -------------
# Client errors
# -------------

CODE_CLIENT_ERROR = 400
CODE_BAD_REQUEST = CODE_CLIENT_ERROR
CODE_UNAUTHORIZED = HTTPStatus.UNAUTHORIZED
CODE_PAYMENT_REQUIRED = HTTPStatus.PAYMENT_REQUIRED
CODE_FORBIDDEN = HTTPStatus.FORBIDDEN
CODE_NOT_FOUND = HTTPStatus.NOT_FOUND
CODE_METHOD_NOT_ALLOWED = HTTPStatus.METHOD_NOT_ALLOWED
CODE_NOT_ACCEPTABLE = HTTPStatus.NOT_ACCEPTABLE
CODE_PROXY_AUTHENTICATION_REQUIRED = HTTPStatus.PROXY_AUTHENTICATION_REQUIRED
CODE_REQUEST_TIMEOUT = HTTPStatus.REQUEST_TIMEOUT
CODE_CONFLICT = HTTPStatus.CONFLICT
CODE_GONE = HTTPStatus.GONE
CODE_LENGTH_REQUIRED = HTTPStatus.LENGTH_REQUIRED
CODE_PRECONDITION_FAILED = HTTPStatus.PRECONDITION_FAILED
CODE_REQUEST_ENTITY_TOO_LARGE = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
CODE_REQUEST_URI_TOO_LONG = HTTPStatus.REQUEST_URI_TOO_LONG
CODE_UNSUPPORTED_MEDIA_TYPE = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
CODE_REQUESTED_RANGE_NOT_SATISFIABLE = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE
CODE_EXPECTATION_FAILED = HTTPStatus.EXPECTATION_FAILED
CODE_MISDIRECTED_REQUEST = HTTPStatus.MISDIRECTED_REQUEST
CODE_UNPROCESSABLE_ENTITY = HTTPStatus.UNPROCESSABLE_ENTITY
CODE_LOCKED = HTTPStatus.LOCKED
CODE_FAILED_DEPENDENCY = HTTPStatus.FAILED_DEPENDENCY
CODE_UPGRADE_REQUIRED = HTTPStatus.UPGRADE_REQUIRED
CODE_PRECONDITION_REQUIRED = HTTPStatus.PRECONDITION_REQUIRED
CODE_TOO_MANY_REQUESTS = HTTPStatus.TOO_MANY_REQUESTS
CODE_REQUEST_HEADER_FIELDS_TOO_LARGE = HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE
CODE_UNAVAILABLE_FOR_LEGAL_REASONS = HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS

# -------------
# Server errors
# -------------

CODE_SERVER_ERROR = 500
CODE_INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR
CODE_NOT_IMPLEMENTED = HTTPStatus.NOT_IMPLEMENTED
CODE_BAD_GATEWAY = HTTPStatus.BAD_GATEWAY
CODE_SERVICE_UNAVAILABLE = HTTPStatus.SERVICE_UNAVAILABLE
CODE_GATEWAY_TIMEOUT = HTTPStatus.GATEWAY_TIMEOUT
CODE_HTTP_VERSION_NOT_SUPPORTED = HTTPStatus.HTTP_VERSION_NOT_SUPPORTED
CODE_VARIANT_ALSO_NEGOTIATES = HTTPStatus.VARIANT_ALSO_NEGOTIATES
CODE_INSUFFICIENT_STORAGE = HTTPStatus.INSUFFICIENT_STORAGE
CODE_LOOP_DETECTED = HTTPStatus.LOOP_DETECTED
CODE_NOT_EXTENDED = HTTPStatus.NOT_EXTENDED
CODE_NETWORK_AUTHENTICATION_REQUIRED = HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED

assert CODE_INFORMATIONAL_RESPONSE == CODE_CONTINUE
assert CODE_SUCCESSFUL == CODE_OK
assert CODE_REDIRECTION == CODE_MULTIPLE_CHOICES
assert CODE_CLIENT_ERROR == CODE_BAD_REQUEST
assert CODE_SERVER_ERROR == CODE_INTERNAL_SERVER_ERROR


class HttpStatus(ReccBaseException):
    def __init__(self, *args, code):
        super().__init__(*args, code=code)
        assert self.is_http_status()


class HttpInformationalResponse(HttpStatus):
    def __init__(self, *args, code=CODE_INFORMATIONAL_RESPONSE):
        super().__init__(*args, code=code)
        assert self.is_informational_response()


class HttpContinue(HttpInformationalResponse):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_CONTINUE)


class HttpSwitchingProtocols(HttpInformationalResponse):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_SWITCHING_PROTOCOLS)


class HttpPROCESSING(HttpInformationalResponse):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_PROCESSING)


class HttpSuccessful(HttpStatus):
    def __init__(self, *args, code=CODE_SUCCESSFUL):
        super().__init__(*args, code=code)
        assert self.is_successful()


class HttpOk(HttpSuccessful):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_OK)


class HttpCreated(HttpSuccessful):
    def __init__(self, *args, code=CODE_CREATED):
        super().__init__(*args, code=code)


class HttpAccepted(HttpSuccessful):
    def __init__(self, *args, code=CODE_ACCEPTED):
        super().__init__(*args, code=code)


class HttpNonAuthoritativeInformation(HttpSuccessful):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_NON_AUTHORITATIVE_INFORMATION)


class HttpNoContent(HttpSuccessful):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_NO_CONTENT)


class HttpResetContent(HttpSuccessful):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RESET_CONTENT)


class HttpPartialContent(HttpSuccessful):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_PARTIAL_CONTENT)


class HttpMultiStatus(HttpSuccessful):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_MULTI_STATUS)


class HttpAlreadyReported(HttpSuccessful):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_ALREADY_REPORTED)


class HttpImUsed(HttpSuccessful):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_IM_USED)


class HttpRedirection(HttpStatus):
    def __init__(self, *args, code=CODE_REDIRECTION):
        super().__init__(*args, code=code)
        assert self.is_redirection()


class HttpMultipleChoices(HttpRedirection):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_MULTIPLE_CHOICES)


class HttpMovedPermanently(HttpRedirection):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_MOVED_PERMANENTLY)


class HttpFound(HttpRedirection):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_FOUND)


class HttpSeeOther(HttpRedirection):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_SEE_OTHER)


class HttpNotModified(HttpRedirection):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_NOT_MODIFIED)


class HttpUseProxy(HttpRedirection):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_USE_PROXY)


class HttpTemporaryRedirect(HttpRedirection):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_TEMPORARY_REDIRECT)


class HttpPermanentRedirect(HttpRedirection):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_PERMANENT_REDIRECT)


class HttpClientError(HttpStatus):
    def __init__(self, *args, code=CODE_CLIENT_ERROR):
        super().__init__(*args, code=code)
        assert self.is_client_error()


class HttpBadRequest(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_BAD_REQUEST)


class HttpUnauthorized(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_UNAUTHORIZED)


class HttpPaymentRequired(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_PAYMENT_REQUIRED)


class HttpForbidden(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_FORBIDDEN)


class HttpNotFound(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_NOT_FOUND)


class HttpMethodNotAllowed(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_METHOD_NOT_ALLOWED)


class HttpNotAcceptable(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_NOT_ACCEPTABLE)


class HttpProxyAuthenticationRequired(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_PROXY_AUTHENTICATION_REQUIRED)


class HttpRequestTimeout(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_REQUEST_TIMEOUT)


class HttpConflict(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_CONFLICT)


class HttpGone(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_GONE)


class HttpLengthRequired(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_LENGTH_REQUIRED)


class HttpPreconditionFailed(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_PRECONDITION_FAILED)


class HttpRequestEntityTooLarge(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_REQUEST_ENTITY_TOO_LARGE)


class HttpRequestUriTooLong(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_REQUEST_URI_TOO_LONG)


class HttpUnsupportedMediaType(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_UNSUPPORTED_MEDIA_TYPE)


class HttpRequestedRangeNotSatisfiable(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_REQUESTED_RANGE_NOT_SATISFIABLE)


class HttpExpectationFailed(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_EXPECTATION_FAILED)


class HttpMisdirectedRequest(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_MISDIRECTED_REQUEST)


class HttpUnprocessableEntity(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_UNPROCESSABLE_ENTITY)


class HttpLocked(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_LOCKED)


class HttpFailedDependency(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_FAILED_DEPENDENCY)


class HttpUpgradeRequired(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_UPGRADE_REQUIRED)


class HttpPreconditionRequired(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_PRECONDITION_REQUIRED)


class HttpTooManyRequests(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_TOO_MANY_REQUESTS)


class HttpRequestHeaderFieldsTooLarge(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_REQUEST_HEADER_FIELDS_TOO_LARGE)


class HttpUnavailableForLegalReasons(HttpClientError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_UNAVAILABLE_FOR_LEGAL_REASONS)


class HttpServerError(HttpStatus):
    def __init__(self, *args, code=CODE_SERVER_ERROR):
        super().__init__(*args, code=code)
        assert self.is_server_error()


class HttpInternalServerError(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_INTERNAL_SERVER_ERROR)


class HttpNotImplemented(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_NOT_IMPLEMENTED)


class HttpBadGateway(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_BAD_GATEWAY)


class HttpServiceUnavailable(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_SERVICE_UNAVAILABLE)


class HttpGatewayTimeout(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_GATEWAY_TIMEOUT)


class HttpHttpVersionNotSupported(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_HTTP_VERSION_NOT_SUPPORTED)


class HttpVariantAlsoNegotiates(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_VARIANT_ALSO_NEGOTIATES)


class HttpInsufficientStorage(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_INSUFFICIENT_STORAGE)


class HttpLoopDetected(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_LOOP_DETECTED)


class HttpNotExtended(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_NOT_EXTENDED)


class HttpNetworkAuthenticationRequired(HttpServerError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_NETWORK_AUTHENTICATION_REQUIRED)
