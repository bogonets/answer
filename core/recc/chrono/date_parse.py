# -*- coding: utf-8 -*-

from typing import Final
from datetime import date

YYYY_MM_DD_TEMPLATE: Final[str] = "YYYY-MM-DD"
YYYY_MM_DD_TEMPLATE_LEN: Final[int] = len(YYYY_MM_DD_TEMPLATE)
DEFAULT_DATE_SEPARATOR: Final[str] = "-"


def parse_yyyy_mm_dd(text: str, separator=DEFAULT_DATE_SEPARATOR) -> date:
    """
    Parse the format 'YYYY-MM-DD' as 'date'.
    """

    if len(text) != YYYY_MM_DD_TEMPLATE_LEN:
        raise ValueError(
            f"The `text` argument must be {YYYY_MM_DD_TEMPLATE_LEN} characters long"
        )
    if text[4] != separator:
        raise ValueError(f"The separator must be `{separator}`")
    if text[7] != separator:
        raise ValueError(f"The separator must be `{separator}`")

    yyyy = text[0:4]
    mm = text[5:7]
    dd = text[8:10]

    if not yyyy.isdigit():
        raise ValueError("The `yyyy` must be a digit")
    if not mm.isdigit():
        raise ValueError("The `mm` must be a digit")
    if not dd.isdigit():
        raise ValueError("The `dd` must be a digit")

    return date(year=int(yyyy), month=int(mm), day=int(dd))
