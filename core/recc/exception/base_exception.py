# -*- coding: utf-8 -*-

UNKNOWN_CODE = -1
CODE_RECC_MIN = 0
CODE_RECC_MAX = 99
CODE_CONTINUE_MIN = 100
CODE_CONTINUE_MAX = 199
CODE_OK_MIN = 200
CODE_OK_MAX = 299
CODE_MULTIPLE_CHOICES_MIN = 300
CODE_MULTIPLE_CHOICES_MAX = 399
CODE_BAD_REQUEST_MIN = 400
CODE_BAD_REQUEST_MAX = 499
CODE_SERVER_ERROR_MIN = 500
CODE_SERVER_ERROR_MAX = 599

CODE_HTTP_MIN = CODE_CONTINUE_MIN
CODE_HTTP_MAX = CODE_SERVER_ERROR_MAX


class ReccBaseException(Exception):
    def __init__(self, *args, code=UNKNOWN_CODE):
        super().__init__(*args)
        self._code = code

    @property
    def code(self) -> int:
        return self._code

    def is_unknown_code(self) -> bool:
        return self._code == UNKNOWN_CODE

    def is_http_status(self) -> bool:
        return CODE_HTTP_MIN <= self._code <= CODE_HTTP_MAX

    def is_informational_response(self) -> bool:
        """
        1xx informational response.
        the request was received, continuing process
        """
        return CODE_CONTINUE_MIN <= self._code <= CODE_CONTINUE_MAX

    def is_successful(self) -> bool:
        """
        2xx successful.
        the request was successfully received, understood, and accepted
        """
        return CODE_OK_MIN <= self._code <= CODE_OK_MAX

    def is_redirection(self) -> bool:
        """
        3xx redirection.
        further action needs to be taken in order to complete the request
        """
        return CODE_MULTIPLE_CHOICES_MIN <= self._code <= CODE_MULTIPLE_CHOICES_MAX

    def is_client_error(self) -> bool:
        """
        4xx client error.
        the request contains bad syntax or cannot be fulfilled
        """
        return CODE_BAD_REQUEST_MIN <= self._code <= CODE_BAD_REQUEST_MAX

    def is_server_error(self) -> bool:
        """
        5xx server error.
        the server failed to fulfil an apparently valid request
        """
        return CODE_SERVER_ERROR_MIN <= self._code <= CODE_SERVER_ERROR_MAX

    def is_recc_code(self) -> bool:
        """
        0xx RECC server code.
        List of errors used internally by the server.
        When responding to HTTP, it should be treated with a different status code.
        """
        return CODE_RECC_MIN <= self._code <= CODE_RECC_MAX
