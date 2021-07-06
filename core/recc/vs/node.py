# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Union, Any
from recc.vs.lamda_interface import LamdaInterface, Lamda
from recc.vs.slot import Slot, SlotKey
from recc.vs.slot_machine import SlotMachine

_ASSERT_MSG_NOT_IN_BEGIN_NODE = "There are no in-flow-slot in begin-node"
_ASSERT_MSG_NOT_IN_END_NODE = "There are no out-flow-slot in end-node"


class NodeEdge(Enum):
    Begin = 0
    Middle = 1
    End = 2

    @classmethod
    def from_str(cls, text: str) -> "NodeEdge":
        key = text[0].upper() + text[1:].lower()
        enums = [s for s in dir(cls) if not s.startswith("_")]
        if key in enums:
            return getattr(cls, key)
        raise KeyError(f"Not found '{key}' enum in {cls.__name__}")


NODE_EDGE_NAME = str(NodeEdge.__name__)
NODE_EDGE_NAME_LEN = len(NODE_EDGE_NAME)
NODE_EDGE_NAME_AND_DOT_LEN = NODE_EDGE_NAME_LEN + len(".")


class Node:
    def __init__(
        self,
        key: int,
        name: str,
        edge: NodeEdge,
        lamda: Optional[LamdaInterface] = None,
        data_output_as_flow_output=False,
    ):
        self._key = key
        self._name = name
        self._edge = edge
        self._sm = SlotMachine()
        self._lamda = lamda if lamda else Lamda()
        self._execution_result: Optional[Exception] = None
        self._data_output_as_flow_output = data_output_as_flow_output

    @property
    def key(self) -> int:
        return self._key

    @property
    def name(self) -> str:
        return self._name

    @property
    def edge(self) -> NodeEdge:
        return self._edge

    @property
    def sm(self) -> SlotMachine:
        return self._sm

    @property
    def execution_result(self) -> Optional[Exception]:
        return self._execution_result

    @property
    def data_output_as_flow_output(self) -> bool:
        return self._data_output_as_flow_output

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"Node({self._key})[name={self._name}]"

    def set_execution_result(self, e: Optional[Exception]) -> None:
        self._execution_result = e

    def reset_execution_result(self) -> None:
        self._execution_result = None

    def is_success(self) -> bool:
        return self._execution_result is None

    def is_failure(self) -> bool:
        return not self.is_success()

    def get_slot_count(self) -> int:
        return self._sm.get_slot_count()

    def get_inputs_count(self) -> int:
        return self._sm.get_inputs_count()

    def get_outputs_count(self) -> int:
        return self._sm.get_outputs_count()

    def get_in_flows_count(self) -> int:
        return self._sm.get_in_flows_count()

    def get_out_flows_count(self) -> int:
        return self._sm.get_out_flows_count()

    def get_in_datas_count(self) -> int:
        return self._sm.get_in_datas_count()

    def get_out_datas_count(self) -> int:
        return self._sm.get_out_datas_count()

    def get_slot(self, key: SlotKey) -> Slot:
        return self._sm.get_slot(key)

    def get_slot_by_name(self, slot_name: str) -> Slot:
        return self.get_slot(Slot.create_key(self.name, slot_name))

    def exist_slot(self, key: SlotKey) -> bool:
        return self._sm.exist_slot(key)

    def exist_slot_by_name(self, slot_name: str) -> bool:
        return self.exist_slot(Slot.create_key(self.name, slot_name))

    def add_in_flow(self, slot: Slot) -> None:
        assert self.edge != NodeEdge.Begin, _ASSERT_MSG_NOT_IN_BEGIN_NODE
        self._sm.add_in_flow(slot)

    def add_out_flow(self, slot: Slot) -> None:
        assert self.edge != NodeEdge.End, _ASSERT_MSG_NOT_IN_END_NODE
        self._sm.add_out_flow(slot)

    def add_in_data(self, slot: Slot) -> None:
        self._sm.add_in_data(slot)

    def add_out_data(self, slot: Slot) -> None:
        self._sm.add_out_data(slot)

    def remove_slot(self, key: SlotKey) -> None:
        self._sm.remove_slot(key)

    # Runtime interfaces.

    def request(self, method: str, key: str, value: Any = None, **options) -> Any:
        return self._lamda.request(method, key, value, **options)

    def init(self) -> None:
        self._lamda.init()

    def valid(self) -> bool:
        return self._lamda.valid()

    def destroy(self) -> None:
        self._lamda.destroy()

    def run(self, **kwargs) -> Any:
        return self._lamda.run(**kwargs)


NodeKey = Union[Node, int, str]
