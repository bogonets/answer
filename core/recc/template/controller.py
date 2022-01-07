# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional, List
from recc.serialization.interface import Serializable
from recc.serialization.deserialize import deserialize
from recc.template.control import Control
from recc.template.v1 import keys as v1k
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

    def serialize(self, version: int) -> Any:
        if version == 1:
            return self.serialize_v1()
        else:
            return self.serialize_v2()

    def deserialize(self, version: int, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if version == 1:
            self.deserialize_v1(data)
        else:
            self.deserialize_v2(data)

    def deserialize_v1(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        hint = Optional[List[Control]]
        input_object = data.get(v1k.k_input)
        if input_object:
            if isinstance(input_object, dict):
                input_value = input_object.get(v1k.k_list)
                self.data_inputs = deserialize(1, input_value, list, hint)
            else:
                self.data_inputs = deserialize(1, input_object, list, hint)

        output_object = data.get(v1k.k_output)
        if output_object:
            if isinstance(output_object, dict):
                output_value = output_object.get(v1k.k_list)
                self.data_outputs = deserialize(1, output_value, list, hint)
            else:
                self.data_outputs = deserialize(1, output_object, list, hint)

        # In version 1, use data-output as flow-output.
        self.data_output_as_flow_output = True

    def serialize_v1(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        if self.data_inputs is not None:
            result[v1k.k_input] = {
                v1k.k_dynamic: False,
                v1k.k_method: "numpy",
                v1k.k_list: [i.serialize_v1() for i in self.data_inputs],
            }
        if self.data_outputs is not None:
            result[v1k.k_output] = {
                v1k.k_dynamic: False,
                v1k.k_method: "numpy",
                v1k.k_list: [o.serialize_v1() for o in self.data_outputs],
            }
        return result

    def deserialize_v2(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        hint = Optional[List[Control]]
        # fmt: off
        self.flow_inputs = deserialize(2, data.get(v2k.k_flow_inputs), list, hint)
        self.flow_outputs = deserialize(2, data.get(v2k.k_flow_outputs), list, hint)
        self.data_inputs = deserialize(2, data.get(v2k.k_data_inputs), list, hint)
        self.data_outputs = deserialize(2, data.get(v2k.k_data_outputs), list, hint)
        self.data_output_as_flow_output = deserialize(2, data.get(v2k.k_data_output_as_flow_output), bool)  # noqa
        # fmt: on

    def serialize_v2(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        if self.flow_inputs is not None:
            result[v2k.k_flow_inputs] = [i.serialize_v2() for i in self.flow_inputs]
        if self.flow_outputs is not None:
            result[v2k.k_flow_outputs] = [o.serialize_v2() for o in self.flow_outputs]
        if self.data_inputs is not None:
            result[v2k.k_data_inputs] = [i.serialize_v2() for i in self.data_inputs]
        if self.data_outputs is not None:
            result[v2k.k_data_outputs] = [o.serialize_v2() for o in self.data_outputs]
        if self.data_output_as_flow_output is not None:
            result[v2k.k_data_output_as_flow_output] = self.data_output_as_flow_output
        return result
