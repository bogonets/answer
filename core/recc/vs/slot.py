# -*- coding: utf-8 -*-

from enum import Enum
from typing import Dict, Set, Optional, Union, Any, Tuple
from recc.vs.box import Box
from recc.vs.arc import Arc


class SlotDirection(Enum):
    Input = 0
    Output = 1


SLOT_DIRECTION_NAME = str(SlotDirection.__name__)
SLOT_DIRECTION_NAME_LEN = len(SLOT_DIRECTION_NAME)
SLOT_DIRECTION_NAME_AND_DOT_LEN = SLOT_DIRECTION_NAME_LEN + len(".")


class SlotCategory(Enum):
    Flow = 0
    Data = 1


SLOT_CATEGORY_NAME = str(SlotCategory.__name__)
SLOT_CATEGORY_NAME_LEN = len(SLOT_CATEGORY_NAME)
SLOT_CATEGORY_NAME_AND_DOT_LEN = SLOT_CATEGORY_NAME_LEN + len(".")


class Slot:

    DELIMITER = "."

    def __init__(
        self,
        key: int,
        name: str,
        base_node_key: int,
        base_node_name: str,
        direction: SlotDirection,
        category: SlotCategory,
        *,
        box: Optional[Box] = None,
        optional=False,
    ):
        self._key = key
        self._name = name
        self._base_node_key = base_node_key
        self._base_node_name = base_node_name
        self._direction = direction
        self._category = category

        self._mimes: Set[str] = set()
        self._arcs: Dict[int, Arc] = dict()

        self._box = box if box else Box()
        self._optional = optional

    @property
    def key(self) -> int:
        return self._key

    @property
    def base_node_key(self) -> int:
        return self._base_node_key

    @property
    def base_node_name(self) -> str:
        return self._base_node_name

    @property
    def direction(self) -> SlotDirection:
        return self._direction

    @property
    def direction_name(self) -> str:
        return str(self._direction)[SLOT_DIRECTION_NAME_AND_DOT_LEN:]

    @property
    def category(self) -> SlotCategory:
        return self._category

    @property
    def category_name(self) -> str:
        return str(self._category)[SLOT_CATEGORY_NAME_AND_DOT_LEN:]

    @property
    def name(self) -> str:
        return self._name

    @property
    def fullname(self) -> str:
        return Slot.create_key(self._base_node_name, self._name)

    @property
    def mimes(self) -> Set[str]:
        return self._mimes

    @property
    def arcs(self) -> Dict[int, Arc]:
        return self._arcs

    @property
    def box(self) -> Box:
        return self._box

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        params0 = f"{self.fullname}/{self.category_name}"
        params1 = f"{self.direction_name}/arcs={len(self.arcs)}"
        return f"Slot({self._key})[{params0}/{params1}]"

    def set_optional(self, flag=True) -> None:
        self._optional = flag

    def is_optional(self) -> bool:
        return self._optional

    def is_requirement(self) -> bool:
        return not self._optional

    def set_box(self, box_or_data: Any) -> None:
        if isinstance(box_or_data, Box):
            self._box = box_or_data
        else:
            self._box = Box(data=box_or_data)

    def add_arc(self, arc: Arc) -> None:
        self._arcs[arc.key] = arc

    def add_output_arc(self, arc: Arc) -> None:
        assert (
            self.direction == SlotDirection.Output
        ), "You can connect the output arc only to the output slot."
        assert (
            self.key == arc.back_key
        ), "The slot-key and the arc-back-key must be the same."
        assert (
            self.fullname == arc.back_fullname
        ), "The slot-fullname and the arc-back-fullname must be the same."
        self.add_arc(arc)

    def add_input_arc(self, arc: Arc) -> None:
        assert (
            self.direction == SlotDirection.Input
        ), "You can connect the input arc only to the input slot."
        assert (
            self.key == arc.front_key
        ), "The slot-key and the arc-front-key must be the same."
        assert (
            self.fullname == arc.front_fullname
        ), "The slot-fullname and the arc-front-fullname must be the same."
        self.add_arc(arc)

    def add_input_arc_with_box(self, arc: Arc, box: Box) -> None:
        self.add_input_arc(arc)
        self.set_box(box)

    def remove_arc(self, key: int) -> None:
        del self._arcs[key]

    def add_mime(self, mime: str) -> None:
        self._mimes.add(mime)

    def remove_mime(self, mime: str) -> None:
        self._mimes.remove(mime)

    @staticmethod
    def split_key(name: str) -> Tuple[str, str]:
        names = name.split(Slot.DELIMITER, 2)
        if len(names) != 2:
            raise ValueError(f"ID splitting failed: {names}")
        return names[0], names[1]

    @staticmethod
    def create_key(node: str, slot: str) -> str:
        return f"{node}{Slot.DELIMITER}{slot}"


SlotKey = Union[Slot, int, str]
