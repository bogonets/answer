# -*- coding: utf-8 -*-

from typing import Optional, Any, Union, Tuple
from recc.vs.box import Box


class Arc:

    DELIMITER = "-"

    def __init__(
        self,
        key: int,
        back_key: int,
        front_key: int,
        back_fullname: str,
        front_fullname: str,
        *,
        box: Optional[Box] = None,
    ):
        self._key = key
        self._back_key = back_key
        self._front_key = front_key
        self._back_fullname = back_fullname
        self._front_fullname = front_fullname
        self._box = box if box else Box()

    @property
    def key(self) -> int:
        return self._key

    @property
    def fullname(self) -> str:
        return Arc.merge(self._back_fullname, self._front_fullname)

    @property
    def back_key(self) -> int:
        return self._back_key

    @property
    def front_key(self) -> int:
        return self._front_key

    @property
    def back_fullname(self) -> str:
        return self._back_fullname

    @property
    def front_fullname(self) -> str:
        return self._front_fullname

    @property
    def box(self) -> Box:
        return self._box

    def __str__(self) -> str:
        return self.fullname

    def __repr__(self) -> str:
        return f"Arc({self._key})[{self.fullname}]"

    def set_box(self, box_or_data: Any) -> None:
        if isinstance(box_or_data, Box):
            self._box = box_or_data
        else:
            self._box = Box(data=box_or_data)

    @staticmethod
    def split(name: str) -> Tuple[str, str]:
        ids = name.split(Arc.DELIMITER, 2)
        if len(ids) != 2:
            raise ValueError(f"ID splitting failed: {name}")
        return ids[0], ids[1]

    @staticmethod
    def merge(back: str, front: str) -> str:
        return f"{back}{Arc.DELIMITER}{front}"


ArcKey = Union[Arc, int, str]
