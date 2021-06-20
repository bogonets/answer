# -*- coding: utf-8 -*-

from enum import Enum
from typing import Any


class BoxState(Enum):
    Inactive = 0
    Active = 1
    Skip = 2
    Failure = 3


BOX_STATE_NAME = str(BoxState.__name__)
BOX_STATE_NAME_LEN = len(BOX_STATE_NAME)
BOX_STATE_NAME_AND_DOT_LEN = BOX_STATE_NAME_LEN + len(".")


class Box:
    def __init__(self, data: Any = None, state=BoxState.Inactive):
        self._data = data
        self._state = state

    @property
    def data(self) -> Any:
        return self._data

    @property
    def data_type(self) -> type:
        return type(self._data)

    @property
    def data_type_name(self) -> str:
        return self.data_type.__name__

    @property
    def state(self) -> BoxState:
        return self._state

    @property
    def state_name(self) -> str:
        return str(self._state)[BOX_STATE_NAME_AND_DOT_LEN:]

    def __repr__(self) -> str:
        return f"Data<{self.data_type_name}>[{self.state_name}]"

    def inactive(self) -> None:
        self._state = BoxState.Inactive

    def active(self) -> None:
        self._state = BoxState.Active

    def skip(self) -> None:
        self._state = BoxState.Skip

    def failure(self) -> None:
        self._state = BoxState.Failure

    def set_state(self, state: BoxState) -> None:
        self._state = state

    def is_inactive(self) -> bool:
        return self._state == BoxState.Inactive

    def is_active(self) -> bool:
        return self._state == BoxState.Active

    def is_skip(self) -> bool:
        return self._state == BoxState.Skip

    def is_failure(self) -> bool:
        return self._state == BoxState.Failure

    def set_data(self, data: Any) -> None:
        self._data = data

    def exist_data(self) -> bool:
        return self._data is not None


class BoxData(object):

    __slots__ = ("node", "slot", "data")

    node: str
    slot: str
    data: Any

    def __init__(self, node: str, slot: str, data: Any = None):
        self.node = node
        self.slot = slot
        self.data = data


class BoxRequest(object):

    __slots__ = ("node", "slot")

    node: str
    slot: str

    def __init__(self, node: str, slot: str):
        self.node = node
        self.slot = slot
