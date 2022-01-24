# -*- coding: utf-8 -*-

from typing import TypeVar, Generic, List, Iterable
from recc.geometry.primitive.point import Point


_T = TypeVar("_T")


class Polyline(Generic[_T]):

    points: List[Point[_T]]

    def __init__(self, points: Iterable):
        self.points = list(points)


ComplexPolyline = Polyline[complex]
FloatPolyline = Polyline[float]
IntPolyline = Polyline[int]
