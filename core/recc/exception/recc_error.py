# -*- coding: utf-8 -*-

from typing import Type, Dict
from recc.exception.base_exception import ReccBaseException

# x: Success
CODE_RECC_OK = 0
# 1x: Common Errors
CODE_RECC_ERROR = 10
CODE_RECC_INIT_ERROR = 11
# 2x: Value Errors
CODE_RECC_VALUE_ERROR = 20
CODE_RECC_ARGUMENT_ERROR = 21
# 3x: Lookup Errors
CODE_RECC_LOOKUP_ERROR = 30
CODE_RECC_INDEX_ERROR = 31
CODE_RECC_OUT_OF_RANGE_ERROR = CODE_RECC_INDEX_ERROR
CODE_RECC_KEY_ERROR = 32
CODE_RECC_NOT_FOUND_ERROR = 33
CODE_RECC_DUPLICATE_ERROR = 34
CODE_RECC_ALREADY_ERROR = 35
CODE_RECC_NOT_READY_ERROR = 36
CODE_RECC_STATE_ERROR = 37
CODE_RECC_TIMEOUT_ERROR = 38
# 4x: Syntax Errors
CODE_RECC_SYNTAX_ERROR = 40
CODE_RECC_PARSING_ERROR = CODE_RECC_SYNTAX_ERROR
CODE_RECC_DECODE_ERROR = 41
CODE_RECC_ENCODE_ERROR = 42
CODE_RECC_OPERATOR_ERROR = 43
CODE_RECC_SERIALIZE_ERROR = 44
CODE_RECC_DESERIALIZE_ERROR = 45
# 5x: Communication Errors
CODE_RECC_COMMUNICATION_ERROR = 50
CODE_RECC_RPC_REQUEST_ERROR = 51
CODE_RECC_RPC_RESPONSE_ERROR = 52
# 6x: Permission Errors
CODE_RECC_PERMISSION_ERROR = 60
CODE_RECC_NO_READABLE_ERROR = 61
CODE_RECC_NO_WRITABLE_ERROR = 62
CODE_RECC_NO_EXECUTABLE_ERROR = 63
CODE_RECC_AUTH_ERROR = 64
# 7x: Runtime Errors
CODE_RECC_RUNTIME_ERROR = 70
CODE_RECC_ABNORMAL_TERMINATION_ERROR = 71


class ReccOk(ReccBaseException):
    def __init__(self, *args, code=CODE_RECC_OK):
        super().__init__(*args, code=code)
        assert self.is_recc_code()


class ReccError(ReccBaseException):
    def __init__(self, *args, code=CODE_RECC_ERROR):
        super().__init__(*args, code=code)
        assert self.is_recc_code()


class ReccInitError(ReccError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_INIT_ERROR)


class ReccValueError(ReccError):
    def __init__(self, *args, code=CODE_RECC_VALUE_ERROR):
        super().__init__(*args, code=code)


class ReccArgumentError(ReccValueError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_ARGUMENT_ERROR)


class ReccLookupError(ReccError):
    def __init__(self, *args, code=CODE_RECC_LOOKUP_ERROR):
        super().__init__(*args, code=code)


class ReccIndexError(ReccLookupError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_INDEX_ERROR)


ReccOutOfRangeError = Type[ReccIndexError]


class ReccKeyError(ReccLookupError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_KEY_ERROR)


class ReccNotFoundError(ReccLookupError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_NOT_FOUND_ERROR)


class ReccDuplicateError(ReccLookupError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_DUPLICATE_ERROR)


class ReccAlreadyError(ReccLookupError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_ALREADY_ERROR)


class ReccNotReadyError(ReccLookupError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_NOT_READY_ERROR)


class ReccStateError(ReccLookupError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_STATE_ERROR)


class ReccTimeoutError(ReccLookupError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_TIMEOUT_ERROR)


class ReccSyntaxError(ReccError):
    def __init__(self, *args, code=CODE_RECC_SYNTAX_ERROR):
        super().__init__(*args, code=code)


ReccParsingError = Type[ReccSyntaxError]


class ReccDecodeError(ReccSyntaxError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_DECODE_ERROR)


class ReccEncodeError(ReccSyntaxError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_ENCODE_ERROR)


class ReccOperatorError(ReccSyntaxError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_OPERATOR_ERROR)


class ReccSerializeError(ReccSyntaxError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_SERIALIZE_ERROR)


class ReccDeserializeError(ReccSyntaxError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_DESERIALIZE_ERROR)


class ReccCommunicationError(ReccError):
    def __init__(self, *args, code=CODE_RECC_COMMUNICATION_ERROR):
        super().__init__(*args, code=code)


class ReccRpcRequestError(ReccCommunicationError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_RPC_REQUEST_ERROR)


class ReccRpcResponseError(ReccCommunicationError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_RPC_RESPONSE_ERROR)


class ReccPermissionError(ReccError):
    def __init__(self, *args, code=CODE_RECC_PERMISSION_ERROR):
        super().__init__(*args, code=code)


class ReccNoReadableError(ReccPermissionError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_NO_READABLE_ERROR)


class ReccNoWritableError(ReccPermissionError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_NO_WRITABLE_ERROR)


class ReccNoExecutableError(ReccPermissionError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_NO_EXECUTABLE_ERROR)


class ReccAuthError(ReccPermissionError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_AUTH_ERROR)


class ReccRuntimeError(ReccError):
    def __init__(self, *args, code=CODE_RECC_RUNTIME_ERROR):
        super().__init__(*args, code=code)


class ReccAbnormalTerminationError(ReccRuntimeError):
    def __init__(self, *args):
        super().__init__(*args, code=CODE_RECC_ABNORMAL_TERMINATION_ERROR)


def get_recc_code_to_error_type_map() -> Dict[int, Type[ReccBaseException]]:
    from inspect import getmembers, isclass
    from sys import modules

    def _is_recc_error_type(x) -> bool:
        return isclass(x) and issubclass(x, ReccBaseException)

    result = dict()
    class_members = getmembers(modules[__name__], _is_recc_error_type)
    for member in class_members:
        class_name = member[0]
        class_type = member[1]
        assert isinstance(class_name, str)
        assert isinstance(class_type, type)
        assert issubclass(class_type, ReccBaseException)
        instance: ReccBaseException = class_type()
        assert instance.is_unknown_code() or instance.is_recc_code()
        result[instance.code] = class_type
    return result


RECC_CODE_TO_ERROR_TYPE_MAP = get_recc_code_to_error_type_map()
