# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List, Tuple
from recc.serialization.utils import update_dict
from recc.serialization.interface import Serializable
from recc.serialization.serialize import serialize
from recc.serialization.deserialize import deserialize
from recc.template.information import Information, EDGE_BEGIN, EDGE_MIDDLE, EDGE_END
from recc.template.runtime_information import RuntimeInformation
from recc.template.controller import Controller
from recc.template.property import Property
from recc.template.v1 import keys as v1k
from recc.template.v2 import keys as v2k

DEFAULT_VERSION_TUPLE = (1, 0)
DEFAULT_SERIALIZABLE_VERSION = DEFAULT_VERSION_TUPLE[0]


class LamdaTemplate(Serializable):

    version: Optional[str] = None
    """Template version.
    """

    information: Optional[Information] = None
    """Information section.
    """

    controller: Optional[Controller] = None
    """Controller section.
    """

    properties: Optional[List[Property]] = None
    """Properties section.
    """

    _runtime_information: Optional[RuntimeInformation] = None
    """Runtime information section.

    .. warning::
        Do not remove the '_' prefix.
        This member variable is not subject to serialization.
    """

    # Don't use the `@property` decorator.
    # During serialization, errors may occur.

    def get_runtime_information(self) -> Optional[RuntimeInformation]:
        return self._runtime_information

    def set_runtime_information(self, info: RuntimeInformation) -> None:
        self._runtime_information = info

    def get_version_tuple(self) -> Tuple[int, int]:
        try:
            versions = [x for x in str(self.version).split(".")]
            if len(versions) == 0:
                return DEFAULT_VERSION_TUPLE
            elif len(versions) == 1:
                return int(versions[0]), 0
            else:
                assert len(versions) >= 2
                return int(versions[0]), int(versions[1])
        except:  # noqa
            return DEFAULT_VERSION_TUPLE

    def get_documentation(self, language: Optional[str] = None) -> Optional[str]:
        if self.information is None:
            return None
        if not self.information.documentations:
            return None
        if language:
            return self.information.documentations[language]
        else:
            return next(iter(self.information.documentations))

    def get_runtime_script_path(self) -> Optional[str]:
        if not self._runtime_information:
            return None
        return self._runtime_information.script_path

    def get_optimize(self) -> int:
        if not self._runtime_information:
            return -1
        if self._runtime_information.optimize is None:
            return -1
        return self._runtime_information.optimize

    def get_script_content(self) -> Optional[str]:
        if not self._runtime_information:
            return None
        return self._runtime_information.script_content

    def get_environment_root(self) -> Optional[str]:
        if not self._runtime_information:
            return None
        if not self._runtime_information.venv:
            return None
        return self._runtime_information.venv.root

    def is_pyenv_environment(self) -> bool:
        if not self.information:
            return False
        if not self.information.environment:
            return False
        return self.information.environment.is_pyenv()

    def get_edge(self) -> str:
        if self.get_version_tuple() >= (2, 0):
            if not self.information:
                return EDGE_MIDDLE
            if not self.information.edge:
                return EDGE_MIDDLE
            return self.information.edge

        if not self.controller:
            return EDGE_BEGIN

        if self.controller.data_inputs:
            if self.controller.data_outputs:
                return EDGE_MIDDLE
            else:
                return EDGE_END
        else:
            if self.controller.data_outputs:
                return EDGE_BEGIN
            else:
                return EDGE_BEGIN

    def get_data_output_as_flow_output(self) -> bool:
        if not self.controller:
            return False
        if self.controller.data_output_as_flow_output is None:
            return False
        return self.controller.data_output_as_flow_output

    # Serializable

    def clear(self) -> None:
        self.version = None
        self.information = None
        self.controller = None
        self.properties = None

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
        self.version = "1.0"

        self.information = Information()
        self.information.deserialize(1, data.get(v1k.k_info))

        self.controller = Controller()
        self.controller.deserialize(1, data.get(v1k.k_controls))

        properties_val = data.get(v1k.k_props)
        properties_hint = Optional[List[Property]]
        self.properties = deserialize(1, properties_val, list, properties_hint)

    def serialize_v1(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        if self.information is not None:
            result[v1k.k_info] = serialize(1, self.information)
        if self.controller is not None:
            result[v1k.k_controls] = serialize(1, self.controller)
        if self.properties is not None:
            result[v1k.k_props] = serialize(1, self.properties)
        else:
            result[v1k.k_props] = list()
        return result

    def deserialize_v2(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        self.version = data.get(v2k.k_version)

        self.information = Information()
        self.information.deserialize(2, data.get(v2k.k_information))

        self.controller = Controller()
        self.controller.deserialize(2, data.get(v2k.k_controller))

        properties_val = data.get(v2k.k_properties)
        properties_hint = Optional[List[Property]]
        self.properties = deserialize(2, properties_val, list, properties_hint)

    def serialize_v2(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_version, self.version)
        if self.information is not None:
            result[v2k.k_information] = serialize(2, self.information)
        if self.controller is not None:
            result[v2k.k_controller] = serialize(2, self.controller)
        if self.properties is not None:
            result[v2k.k_properties] = serialize(2, self.properties)
        return result
