# -*- coding: utf-8 -*-

from enum import Enum


class AccessAttribute(Enum):
    Anonymous = 0
    HasAdmin = 1

    HasGroupCreate = 2
    HasGroupRead = 3
    HasGroupUpdate = 4
    HasGroupDelete = 5

    HasProjectCreate = 6
    HasProjectRead = 7
    HasProjectUpdate = 8
    HasProjectDelete = 9


aa = AccessAttribute
