# -*- coding: utf-8 -*-

from re import compile as re_compile
from datetime import timedelta

NUMBER_REGX = re_compile(r"^[0-9]+\.?[0-9]*")


def duration_to_timedelta(duration: str) -> timedelta:
    match = NUMBER_REGX.match(duration.strip())
    if match is None:
        raise ValueError("The `duration` argument must contain a number.")

    begin = match.pos
    end = match.end()
    number = float(duration[begin:end])

    unit_original = duration[end:].strip()
    u = unit_original.lower()

    if len(u) == 0:
        raise ValueError("The `duration` argument must contain a unit.")

    if len(u) == 1:
        if u == "w":
            return timedelta(weeks=number)
        if u == "d":
            return timedelta(days=number)
        if u == "h":
            return timedelta(hours=number)
        if u == "m":
            return timedelta(minutes=number)
        if u == "s":
            return timedelta(seconds=number)
        else:
            raise ValueError(f"Unknown unit: ${unit_original}")

    assert len(u) >= 2
    if u == "week" or u == "weeks":
        return timedelta(weeks=number)
    if u == "day" or u == "days":
        return timedelta(days=number)
    if u == "hour" or u == "hours":
        return timedelta(hours=number)
    if u == "min" or u == "minute" or u == "minutes":
        return timedelta(minutes=number)
    if u == "sec" or u == "second" or u == "seconds":
        return timedelta(seconds=number)
    if u == "micro" or u == "microsecond" or u == "microseconds":
        return timedelta(microseconds=number)
    if u == "milli" or u == "millisecond" or u == "milliseconds":
        return timedelta(milliseconds=number)

    raise ValueError(f"Unknown unit: ${unit_original}")
