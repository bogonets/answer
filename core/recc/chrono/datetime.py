# -*- coding: utf-8 -*-

from datetime import datetime


def today() -> datetime:
    return datetime.now().astimezone()
