# -*- coding: utf-8 -*-

from typing import Union, Optional, Callable, Final
from functools import wraps
from logging import Logger
from time import time
from inspect import iscoroutinefunction
from recc.logging.logging import get_logger, convert_level_number

LoggingElapsedCallable = Callable[[str, float], None]

DEFAULT_ROUND_PRECISION: Final[int] = 3


def _logging_elapsed_seconds(
    function_name: str,
    elapsed: float,
    logger: Optional[Union[str, Logger]] = None,
    level: Optional[Union[str, int]] = None,
    callback: Optional[LoggingElapsedCallable] = None,
    round_precision: Optional[int] = None,
) -> None:
    if round_precision is not None:
        elapsed_seconds = round(elapsed, round_precision)
    else:
        elapsed_seconds = elapsed

    if callback:
        callback(function_name, elapsed_seconds)
        return

    _logger = get_logger(logger)
    _level = convert_level_number(level)

    _logger.log(
        _level,
        f"Elapsed time of function `{function_name}` is {elapsed_seconds} seconds",
    )


def logging_elapsed(
    logger: Optional[Union[str, Logger]] = None,
    level: Optional[Union[str, int]] = None,
    callback: Optional[LoggingElapsedCallable] = None,
    round_precision: Optional[int] = DEFAULT_ROUND_PRECISION,
):
    def _wrapper(func):
        if iscoroutinefunction(func):

            @wraps(func)
            async def _wrap1(*args, **kwargs):
                _begin = time()
                result = await func(*args, **kwargs)
                _logging_elapsed_seconds(
                    func.__name__,
                    time() - _begin,
                    logger,
                    level,
                    callback,
                    round_precision,
                )
                return result

            return _wrap1
        else:

            @wraps(func)
            def _wrap2(*args, **kwargs):
                _begin = time()
                result = func(*args, **kwargs)
                _logging_elapsed_seconds(
                    func.__name__,
                    time() - _begin,
                    logger,
                    level,
                    callback,
                    round_precision,
                )
                return result

            return _wrap2

    return _wrapper
