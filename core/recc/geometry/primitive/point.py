# -*- coding: utf-8 -*-

from typing import Generic, TypeVar

_T = TypeVar("_T")


class Point(Generic[_T]):
    def __init__(self, x: _T, y: _T):
        self.x = x
        self.y = y


ComplexPoint = Point[complex]
FloatPoint = Point[float]
IntPoint = Point[int]
