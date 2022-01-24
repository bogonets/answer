# -*- coding: utf-8 -*-

from typing import TypeVar, Generic
from recc.geometry.primitive.point import Point

_T = TypeVar("_T")


class Line(Generic[_T]):

    p1: Point[_T]
    p2: Point[_T]

    def __init__(self, x1: _T, y1: _T, x2: _T, y2: _T):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)

    @property
    def x1(self) -> _T:
        return self.p1.x

    @x1.setter
    def x1(self, value: _T) -> None:
        self.p1.x = value

    @property
    def y1(self) -> _T:
        return self.p1.y

    @y1.setter
    def y1(self, value: _T) -> None:
        self.p1.y = value

    @property
    def x2(self) -> _T:
        return self.p2.x

    @x2.setter
    def x2(self, value: _T) -> None:
        self.p2.x = value

    @property
    def y2(self) -> _T:
        return self.p2.y

    @y2.setter
    def y2(self, value: _T) -> None:
        self.p2.y = value


ComplexLine = Line[complex]
FloatLine = Line[float]
IntLine = Line[int]
