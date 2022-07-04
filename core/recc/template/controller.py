# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional

from type_serialize import Serializable, deserialize

from recc.template.control import Control
from recc.template.v2 import keys as v2k


class Controller(Serializable):
    flow_inputs: Optional[List[Control]] = None
    flow_outputs: Optional[List[Control]] = None
    data_inputs: Optional[List[Control]] = None
    data_outputs: Optional[List[Control]] = None
    data_output_as_flow_output: Optional[bool] = None

    def clear(self) -> None:
        self.data_inputs = None
        self.data_outputs = None

    def __serialize__(self) -> Any:
        result: Dict[str, Any] = dict()
        if self.flow_inputs is not None:
            result[v2k.k_flow_inputs] = [i.__serialize__() for i in self.flow_inputs]
        if self.flow_outputs is not None:
            result[v2k.k_flow_outputs] = [o.__serialize__() for o in self.flow_outputs]
        if self.data_inputs is not None:
            result[v2k.k_data_inputs] = [i.__serialize__() for i in self.data_inputs]
        if self.data_outputs is not None:
            result[v2k.k_data_outputs] = [o.__serialize__() for o in self.data_outputs]
        if self.data_output_as_flow_output is not None:
            result[v2k.k_data_output_as_flow_output] = self.data_output_as_flow_output
        return result

    def __deserialize__(self, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if not isinstance(data, dict):
            raise TypeError
        hint = Optional[List[Control]]
        # fmt: off
        self.flow_inputs = deserialize(data.get(v2k.k_flow_inputs), hint)
        self.flow_outputs = deserialize(data.get(v2k.k_flow_outputs), hint)
        self.data_inputs = deserialize(data.get(v2k.k_data_inputs), hint)
        self.data_outputs = deserialize(data.get(v2k.k_data_outputs), hint)
        self.data_output_as_flow_output = deserialize(data.get(v2k.k_data_output_as_flow_output), bool)  # noqa
        # fmt: on
