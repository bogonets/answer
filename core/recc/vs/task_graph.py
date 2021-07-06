# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Any, Iterable
from functools import reduce
from recc.exception.recc_error import ReccArgumentError
from recc.mime.mime_codec_register import MimeCodecRegister, get_global_mime_register
from recc.mime.mime_codec import MimeEncoder, MimeDecoder
from recc.sequence.sequencer_interface import SequencerInterface
from recc.sequence.default_sequencer import DefaultSequencer
from recc.blueprint.blueprint import BpTask
from recc.template.manager.lamda_template_manager import LamdaTemplateManager
from recc.template.information import EDGE_BEGIN, EDGE_MIDDLE, EDGE_END
from recc.serializable.json import deserialize_json_text
from recc.vs.box import BoxState, BoxData, BoxRequest
from recc.vs.arc import Arc, ArcKey
from recc.vs.slot import SlotDirection, SlotCategory, Slot, SlotKey
from recc.vs.slot_machine import SlotMachine
from recc.vs.node import NodeEdge, Node, NodeKey
from recc.vs.lamda_interface import REQUEST_METHOD_SET, REQUEST_METHOD_GET, Lamda
from recc.vs.lamda_python import LamdaPython
from recc.vs.signal import Signal, SignalResult

_ERR_MSG_NO_IFC_NAME = "Some of the input flow controllers are unnamed."
_ERR_MSG_NO_OFC_NAME = "Some of the output flow controllers are unnamed."
_ERR_MSG_NO_IDC_NAME = "Some of the input data controllers are unnamed."
_ERR_MSG_NO_ODC_NAME = "Some of the output data controllers are unnamed."

_ERR_MSG_NO_BACK_ARC = "The 'back' arc does not exist."
_ERR_MSG_NO_FRONT_ARC = "The 'front' arc does not exist."
_ERR_MSG_NO_BACK_NODE_NAME = "No node name in 'back' arc."
_ERR_MSG_NO_BACK_SLOT_NAME = "No slot name in 'back' arc."
_ERR_MSG_NO_FRONT_NODE_NAME = "No node name in 'front' arc."
_ERR_MSG_NO_FRONT_SLOT_NAME = "No slot name in 'front' arc."


class TaskGraph:
    def __init__(
        self,
        name: Optional[str] = None,
        *,
        node_sequencer: Optional[SequencerInterface] = None,
        slot_sequencer: Optional[SequencerInterface] = None,
        arc_sequencer: Optional[SequencerInterface] = None,
        mimes: Optional[MimeCodecRegister] = None,
    ):
        self._name = name if name else str()

        self._nodes: Dict[int, Node] = dict()
        self._middles: Dict[int, Node] = dict()
        self._begins: Dict[int, Node] = dict()
        self._ends: Dict[int, Node] = dict()
        self._node_names: Dict[str, Node] = dict()
        self._node_sequencer = node_sequencer if node_sequencer else DefaultSequencer()

        self._sm = SlotMachine()
        self._slot_sequencer = slot_sequencer if slot_sequencer else DefaultSequencer()

        self._arcs: Dict[int, Arc] = dict()
        self._arc_fullnames: Dict[str, Arc] = dict()
        self._arc_sequencer = arc_sequencer if arc_sequencer else DefaultSequencer()

        self._signals: Dict[str, Node] = dict()
        self._mimes = mimes if mimes else get_global_mime_register()

    def clear(self) -> None:
        self._nodes.clear()
        self._middles.clear()
        self._begins.clear()
        self._ends.clear()
        self._node_names.clear()
        self._sm.clear()
        self._arcs.clear()
        self._arc_fullnames.clear()
        self._signals.clear()

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"Task<name={self._name},nodes={len(self._nodes)}>"

    def set_name(self, name: str) -> None:
        self._name = name

    def get_node_count(self) -> int:
        return len(self._nodes)

    def get_middles_count(self) -> int:
        return len(self._middles)

    def get_begins_count(self) -> int:
        return len(self._begins)

    def get_ends_count(self) -> int:
        return len(self._ends)

    def get_node(self, key: NodeKey) -> Node:
        if isinstance(key, Node):
            if key != self._nodes[key.key]:
                raise KeyError(f"Unregistered node object: key={key.key}")
            return key
        elif isinstance(key, int):
            return self._nodes[key]
        elif isinstance(key, str):
            return self._node_names[key]
        else:
            raise KeyError(f"Unsupported key type: {type(key).__name__}")

    def exist_node(self, key: NodeKey) -> bool:
        try:
            self.get_node(key)
            return True
        except KeyError:
            return False

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

    def exist_slot(self, key: SlotKey) -> bool:
        return self._sm.exist_slot(key)

    def get_arc_count(self) -> int:
        return len(self._arcs)

    def get_arc(self, key: ArcKey) -> Arc:
        if isinstance(key, Arc):
            if key != self._arcs[key.key]:
                raise KeyError(f"Unregistered arc object: key={key.key}")
            return key
        elif isinstance(key, int):
            return self._arcs[key]
        elif isinstance(key, str):
            return self._arc_fullnames[key]
        else:
            raise KeyError(f"Unsupported key type: {type(key).__name__}")

    def exist_arc(self, key: ArcKey) -> bool:
        try:
            self.get_arc(key)
            return True
        except KeyError:
            return False

    # Node

    def add_node(
        self,
        name: str,
        edge: NodeEdge,
        impl: Optional[Lamda] = None,
        data_output_as_flow_output=False,
    ) -> Node:
        if name in self._node_names:
            raise ValueError(f"Already exists node name: {name}")

        # The exception shouldn't be thrown until the function ends.

        new_id = self._node_sequencer.next()
        assert new_id not in self._nodes

        node = Node(new_id, name, edge, impl, data_output_as_flow_output)
        if edge == NodeEdge.Middle:
            self._middles[new_id] = node
        elif edge == NodeEdge.Begin:
            self._begins[new_id] = node
        else:
            assert edge == NodeEdge.End
            self._ends[new_id] = node

        self._nodes[new_id] = node
        self._node_names[name] = node
        return node

    def add_middle_node(
        self,
        name: str,
        impl: Optional[Lamda] = None,
        data_output_as_flow_output=False,
    ) -> Node:
        return self.add_node(name, NodeEdge.Middle, impl, data_output_as_flow_output)

    def add_begin_node(
        self,
        name: str,
        impl: Optional[Lamda] = None,
        data_output_as_flow_output=False,
    ) -> Node:
        return self.add_node(name, NodeEdge.Begin, impl, data_output_as_flow_output)

    def add_end_node(
        self,
        name: str,
        impl: Optional[Lamda] = None,
        data_output_as_flow_output=False,
    ) -> Node:
        return self.add_node(name, NodeEdge.End, impl, data_output_as_flow_output)

    def remove_node(self, key: NodeKey) -> None:
        node = self.get_node(key)
        for slot_key, slot_val in node.sm.slots.items():
            for arc_key, _ in slot_val.arcs.items():
                # There is a risk of recursion.
                if arc_key in self._arcs:
                    arc_fullname = self._arcs[arc_key].fullname
                    del self._arc_fullnames[arc_fullname]
                    del self._arcs[arc_key]
            self._sm.remove_slot(slot_key)
        uid = node.key
        edge = node.edge
        name = node.name
        if edge == NodeEdge.Middle:
            del self._middles[uid]
        elif edge == NodeEdge.Begin:
            del self._begins[uid]
        elif edge == NodeEdge.End:
            del self._ends[uid]
        del self._nodes[uid]
        del self._node_names[name]

    # Slot

    @staticmethod
    def _test_add_slot(
        edge: NodeEdge,
        direction: SlotDirection,
        category: SlotCategory,
    ) -> None:
        if category == SlotCategory.Flow:
            if direction == SlotDirection.Input and edge == NodeEdge.Begin:
                raise ValueError("There are no in-flow-slot in begin-node")
            elif direction == SlotDirection.Output and edge == NodeEdge.End:
                raise ValueError("There are no out-flow-slot in end-node")
        else:
            assert category == SlotCategory.Data

    def add_slot(
        self,
        name: str,
        node_key: NodeKey,
        direction: SlotDirection,
        category: SlotCategory,
    ) -> Slot:
        node = self.get_node(node_key)
        self._test_add_slot(node.edge, direction, category)

        if node.exist_slot_by_name(name):
            raise ValueError(f"Already exists slot: node={node.name}/slot={name}")

        # The exception shouldn't be thrown until the function ends.

        new_id = self._slot_sequencer.next()
        assert new_id not in self._sm.slots
        slot = Slot(new_id, name, node.key, node.name, direction, category)
        assert slot.fullname not in self._sm.fullnames

        if direction == SlotDirection.Input:
            if category == SlotCategory.Flow:
                node.add_in_flow(slot)
                self._sm.add_in_flow(slot)
            else:
                assert category == SlotCategory.Data
                node.add_in_data(slot)
                self._sm.add_in_data(slot)
        else:
            assert direction == SlotDirection.Output
            if category == SlotCategory.Flow:
                node.add_out_flow(slot)
                self._sm.add_out_flow(slot)
            else:
                assert category == SlotCategory.Data
                node.add_out_data(slot)
                self._sm.add_out_data(slot)

        return slot

    def add_input_flow_slot(self, name: str, node: NodeKey) -> Slot:
        return self.add_slot(name, node, SlotDirection.Input, SlotCategory.Flow)

    def add_output_flow_slot(self, name: str, node: NodeKey) -> Slot:
        return self.add_slot(name, node, SlotDirection.Output, SlotCategory.Flow)

    def add_input_data_slot(self, name: str, node: NodeKey) -> Slot:
        return self.add_slot(name, node, SlotDirection.Input, SlotCategory.Data)

    def add_output_data_slot(self, name: str, node: NodeKey) -> Slot:
        return self.add_slot(name, node, SlotDirection.Output, SlotCategory.Data)

    def remove_slot(self, key: SlotKey) -> None:
        slot = self.get_slot(key)
        for arc_key, _ in slot.arcs.items():
            # There is a risk of recursion.
            if arc_key in self._arcs:
                fullname = self._arcs[arc_key].fullname
                del self._arc_fullnames[fullname]
                del self._arcs[arc_key]
        self.get_node(slot.base_node_key).remove_slot(slot)
        self._sm.remove_slot(key)

    # Arc

    def add_arc(self, back_key: SlotKey, front_key: SlotKey) -> Arc:
        back_slot = self.get_slot(back_key)
        front_slot = self.get_slot(front_key)

        if back_slot.base_node_key == front_slot.base_node_key:
            raise ValueError("The same node cannot be connected.")

        if back_slot.direction != SlotDirection.Output:
            raise ValueError("Only the output-direction is allowed for the back-slot.")
        if front_slot.direction != SlotDirection.Input:
            raise ValueError("Only the input-direction is allowed for the front-slot.")
        if back_slot.category != front_slot.category:
            raise ValueError(
                "The categories of back-slot and front-slot must be the same."
            )

        category = back_slot.category
        if category == SlotCategory.Flow:
            if len(back_slot.arcs) >= 1:
                raise ValueError("The flow-slot only allows 1 back-slot")
        else:
            assert category == SlotCategory.Data
            if len(front_slot.arcs) >= 1:
                raise ValueError("The data-slot only allows 1 front-slot")

        # The exception shouldn't be thrown until the function ends.

        new_id = self._arc_sequencer.next()
        assert new_id not in self._arcs

        arc = Arc(
            new_id,
            back_slot.key,
            front_slot.key,
            back_slot.fullname,
            front_slot.fullname,
            box=back_slot.box,
        )
        assert arc.fullname not in self._arc_fullnames

        self._arcs[new_id] = arc
        self._arc_fullnames[arc.fullname] = arc
        back_slot.add_output_arc(arc)

        if category == SlotCategory.Data:
            # Boxes that can connect multiple arcs should not be removed.
            # So, you need to share that Box.
            front_slot.add_input_arc_with_box(arc, back_slot.box)
        else:
            # Input-flow-slot can have multiple arcs. So don't share Box.
            front_slot.add_input_arc(arc)

        return arc

    def remove_arc(self, key: ArcKey) -> None:
        arc = self.get_arc(key)
        uid = arc.key
        fullname = arc.fullname
        self.get_slot(arc.back_key).remove_arc(arc.key)
        self.get_slot(arc.front_key).remove_arc(arc.key)
        del self._arc_fullnames[fullname]
        del self._arcs[uid]

    # Blueprint

    def set_blueprint(self, bp_task: BpTask, tm: LamdaTemplateManager) -> None:
        if not bp_task.nodes:
            raise ReccArgumentError("Empty nodes")

        for node_name, bp_node in bp_task.nodes.items():
            template_category = bp_node.template_category
            template_name = bp_node.template_name

            if template_category is None:
                raise ReccArgumentError("Empty template category")
            if template_name is None:
                raise ReccArgumentError("Empty template name")

            template = tm.find_template(template_category, template_name)
            template_edge = template.get_edge()
            if template_edge == EDGE_BEGIN:
                node_edge = NodeEdge.Begin
            elif template_edge == EDGE_MIDDLE:
                node_edge = NodeEdge.Middle
            elif template_edge == EDGE_END:
                node_edge = NodeEdge.End
            else:
                node_edge = NodeEdge.Middle

            impl = LamdaPython(template)
            impl.init_properties(bp_node.properties)
            impl.init()

            data_output_as_flow_output = template.get_data_output_as_flow_output()
            node = self.add_node(node_name, node_edge, impl, data_output_as_flow_output)
            if template.controller:
                if template.controller.flow_inputs:
                    for fi in template.controller.flow_inputs:
                        if not fi.name:
                            raise ReccArgumentError(_ERR_MSG_NO_IFC_NAME)
                        self.add_input_flow_slot(fi.name, node)
                if template.controller.flow_outputs:
                    for fo in template.controller.flow_outputs:
                        if not fo.name:
                            raise ReccArgumentError(_ERR_MSG_NO_OFC_NAME)
                        self.add_output_flow_slot(fo.name, node)

                if template.controller.data_inputs:
                    for di in template.controller.data_inputs:
                        if not di.name:
                            raise ReccArgumentError(_ERR_MSG_NO_IDC_NAME)
                        self.add_input_data_slot(di.name, node)
                if template.controller.data_outputs:
                    for do in template.controller.data_outputs:
                        if not do.name:
                            raise ReccArgumentError(_ERR_MSG_NO_ODC_NAME)
                        self.add_output_data_slot(do.name, node)

        if bp_task.arcs:
            for arc_name, bp_arc in bp_task.arcs.items():
                if not bp_arc.back:
                    raise ReccArgumentError(_ERR_MSG_NO_BACK_ARC)
                if not bp_arc.front:
                    raise ReccArgumentError(_ERR_MSG_NO_FRONT_ARC)

                if not bp_arc.back.node:
                    raise ReccArgumentError(_ERR_MSG_NO_BACK_NODE_NAME)
                if not bp_arc.back.slot:
                    raise ReccArgumentError(_ERR_MSG_NO_BACK_SLOT_NAME)

                if not bp_arc.front.node:
                    raise ReccArgumentError(_ERR_MSG_NO_FRONT_NODE_NAME)
                if not bp_arc.front.slot:
                    raise ReccArgumentError(_ERR_MSG_NO_FRONT_SLOT_NAME)

                back_slot = Slot.create_key(bp_arc.back.node, bp_arc.back.slot)
                front_slot = Slot.create_key(bp_arc.front.node, bp_arc.front.slot)
                self.add_arc(self.get_slot(back_slot), self.get_slot(front_slot))

    def set_blueprint_json(
        self, json_text: str, version: int, tm: LamdaTemplateManager
    ) -> None:
        blueprint = deserialize_json_text(version, json_text, BpTask)
        self.set_blueprint(blueprint, tm)

    # Signal

    def add_signal(self, name: str, node: NodeKey) -> None:
        self._signals[name] = self.get_node(node)

    def remove_signal(self, name: str) -> None:
        del self._signals[name]

    # MIME Codecs

    def add_mime_codec(
        self,
        mime: str,
        encoder: Optional[MimeEncoder] = None,
        decoder: Optional[MimeDecoder] = None,
    ) -> None:
        if self._mimes.exist(mime):
            if encoder and self._mimes.exist_encoder(mime):
                self._mimes.set_encoder(mime, encoder)
            if decoder and self._mimes.exist_decoder(mime):
                self._mimes.set_decoder(mime, decoder)
        else:
            self._mimes.add(mime, encoder=encoder, decoder=decoder)

    def remove_mime_codec(self, mime: str) -> None:
        self._mimes.remove(mime)

    def add_mime(self, slot: SlotKey, mime: str) -> None:
        self.get_slot(slot).add_mime(mime)

    def remove_mime(self, slot: SlotKey, mime: str) -> None:
        self.get_slot(slot).remove_mime(mime)

    def encode(self, data: Any, mime: str) -> bytes:
        return self._mimes.encode(mime, data)

    def decode(self, data: bytes, mime: str) -> Any:
        return self._mimes.decode(mime, data)

    # Node Interface

    def node_set(self, node: NodeKey, key: str, value: Any) -> None:
        self.node_request(node, REQUEST_METHOD_SET, key, value)

    def node_get(self, node: NodeKey, key: str) -> Any:
        return self.node_request(node, REQUEST_METHOD_GET, key)

    def node_request(
        self,
        node: NodeKey,
        method: str,
        key: str,
        value: Optional[Any] = None,
        **options,
    ) -> Any:
        return self.get_node(node).request(method, key, value, **options)

    def node_init(self, node: NodeKey) -> None:
        self.get_node(node).init()

    def node_valid(self, node: NodeKey) -> bool:
        return self.get_node(node).valid()

    def node_destroy(self, node: NodeKey) -> None:
        self.get_node(node).destroy()

    def node_run(self, node: NodeKey, **kwargs) -> Dict[str, Any]:
        return self.get_node(node).run(**kwargs)

    def set_data(self, slot: SlotKey, data: Any):
        self.get_slot(slot).box.set_data(data)

    def get_data(self, slot: SlotKey) -> Any:
        return self.get_slot(slot).box.data

    def _reset_states(self) -> None:
        for _, n in self._nodes.items():
            n.reset_execution_result()
            for _, s in self._sm.slots.items():
                s.box.inactive()

    def get_dataset(self, slot_keys: Iterable[int]) -> Dict[int, Any]:
        return {k: self.get_slot(k).box.data for k in slot_keys}

    @staticmethod
    def _test_input_flow_slots(input_flow_slots: Dict[int, Slot]) -> bool:
        if not input_flow_slots:
            return True
        assert len(input_flow_slots) >= 1
        for k, v in input_flow_slots.items():
            assert v.direction == SlotDirection.Input
            assert v.category == SlotCategory.Flow
            if v.box.is_active():
                return True
        return False

    @staticmethod
    def _get_inactive_input_flow_slots(input_flow_slots: Dict[int, Slot]) -> List[int]:
        result = list()
        for k, v in input_flow_slots.items():
            assert v.direction == SlotDirection.Input
            assert v.category == SlotCategory.Flow
            if v.box.is_inactive():
                result.append(k)
        return result

    def _run_input_data_slots(self, input_data_slots: Dict[int, Slot]) -> List[int]:
        execution_order = list()
        for k, v in input_data_slots.items():
            assert v.direction == SlotDirection.Input
            assert v.category == SlotCategory.Data
            assert len(v.arcs) == 1 or len(v.arcs) == 0

            state = v.box.state
            if state == BoxState.Active:
                continue
            elif state == BoxState.Inactive:
                input_node = self._nodes[v.base_node_key]
                execution_order += self._run_node(input_node)
            elif state == BoxState.Skip:
                continue
            elif state == BoxState.Failure:
                if v.is_requirement():
                    raise RuntimeError(
                        f"A failure flag was detected for a required slot: {v.fullname}"
                    )
            else:
                raise ValueError(f"Unknown state value: {state}")
        return execution_order

    @staticmethod
    def _get_input_data_slots(input_data_slots: Dict[int, Slot]) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        for k, v in input_data_slots.items():
            assert v.direction == SlotDirection.Input
            assert v.category == SlotCategory.Data
            assert len(v.arcs) == 1 or len(v.arcs) == 0

            if v.box.is_active():
                result[v.name] = v.box.data
            else:
                result[v.name] = None
        return result

    def _get_input_flow_slots(
        self, input_flow_slots: Dict[int, Slot]
    ) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        for k, v in input_flow_slots.items():
            assert v.direction == SlotDirection.Input
            assert v.category == SlotCategory.Flow

            if v.name not in result:
                result[v.name] = dict()

            # Input-flow-slot can have multiple arcs.
            # Acquire active data connected to each arc.
            assert isinstance(result[v.name], dict)
            for arc_key, arc_val in v.arcs.items():
                back_flow_slot = self._sm.out_flows[arc_val.back_key]
                back_box = back_flow_slot.box
                back_key = back_flow_slot.fullname
                if back_box.is_active():
                    result[v.name][back_key] = back_box.data
                else:
                    result[v.name][back_key] = None
        return result

    @staticmethod
    def _skip_output_data_slots(output_data_slots: Dict[int, Slot]) -> None:
        for k, v in output_data_slots.items():
            assert v.direction == SlotDirection.Output
            assert v.category == SlotCategory.Data
            v.box.skip()

    @staticmethod
    def _put_output_data_slots(
        execution_result: Dict[str, Any],
        output_data_slots: Dict[int, Slot],
    ) -> None:
        for k, v in output_data_slots.items():
            assert v.direction == SlotDirection.Output
            assert v.category == SlotCategory.Data

            if v.name in execution_result.keys():
                v.box.set_data(execution_result[v.name])
                v.box.active()
            else:
                v.box.skip()

    @staticmethod
    def _put_output_flow_slots(
        execution_result: Dict[str, Any],
        output_flow_slots: Dict[int, Slot],
    ) -> None:
        for k, v in output_flow_slots.items():
            assert v.direction == SlotDirection.Output
            assert v.category == SlotCategory.Flow

            if v.name in execution_result.keys():
                v.box.set_data(execution_result[v.name])
                v.box.active()
            else:
                v.box.skip()

    @staticmethod
    def _failure_output_datas(out_data_slots: Dict[int, Slot]) -> None:
        for k, v in out_data_slots.items():
            assert v.direction == SlotDirection.Output
            assert v.category == SlotCategory.Data
            v.box.failure()

    @staticmethod
    def _failure_output_flows(out_flow_slots: Dict[int, Slot]) -> None:
        for k, v in out_flow_slots.items():
            assert v.direction == SlotDirection.Output
            assert v.category == SlotCategory.Flow
            v.box.failure()

    def _run_output_flow_slots(self, output_flow_slots: Dict[int, Slot]) -> List[int]:
        execution_order = list()
        for k, v in output_flow_slots.items():
            if not v.box.is_active():
                continue

            arcs_count = len(v.arcs)
            if arcs_count == 0:
                continue

            assert arcs_count == 1
            arc = next(iter(v.arcs.values()))
            slot = self._sm.in_flows[arc.front_key]
            node = self._nodes[slot.base_node_key]
            execution_order += self._run_node(node)
        return execution_order

    def _run_output_data_slots(self, output_data_slots: Dict[int, Slot]) -> List[int]:
        execution_order = list()
        for k, v in output_data_slots.items():
            if not v.box.is_active():
                continue

            arcs_count = len(v.arcs)
            if arcs_count == 0:
                continue

            assert arcs_count == 1
            arc = next(iter(v.arcs.values()))
            slot = self._sm.in_datas[arc.front_key]
            node = self._nodes[slot.base_node_key]
            execution_order += self._run_node(node)
        return execution_order

    def _run_node(self, node: Node) -> List[int]:
        execution_order = list()
        in_flows = node.sm.in_flows
        out_flows = node.sm.out_flows
        in_datas = node.sm.in_datas
        out_datas = node.sm.out_datas

        if not self._test_input_flow_slots(in_flows):
            inactive_slot_ids = self._get_inactive_input_flow_slots(in_flows)
            inactive_slots = [str(i) for i in inactive_slot_ids]
            assert len(inactive_slots) >= 1
            inactive_slots_text = reduce(lambda x, y: f"{x},{y}", inactive_slots)
            params_msg = f"Inactive slots: {inactive_slots_text}"
            raise ValueError(f"All input-flow-slots must be active. {params_msg}")

        execution_order += self._run_input_data_slots(in_datas)
        kwargs: Dict[str, Any] = dict()
        kwargs.update(self._get_input_data_slots(in_datas))
        kwargs.update(self._get_input_flow_slots(in_flows))

        try:
            result = node.run(**kwargs)
            if result is None:
                self._skip_output_data_slots(out_datas)
            elif isinstance(result, dict):
                self._put_output_data_slots(result, out_datas)
                self._put_output_flow_slots(result, out_flows)
            else:
                result_type = type(result).__name__
                raise ValueError(f"Unsupported runner's result type: {result_type}")
            execution_order.append(node.key)
            node.reset_execution_result()
        except Exception as e:
            self._failure_output_datas(out_datas)
            self._failure_output_flows(out_flows)
            node.set_execution_result(e)
            return execution_order

        # Use data-output as flow-output.
        if node.data_output_as_flow_output:
            execution_order += self._run_output_data_slots(out_datas)

        return execution_order + self._run_output_flow_slots(out_flows)

    def slot_fullnames_to_ids(self, fullnames: Iterable[str]) -> Iterable[int]:
        return [self._sm.fullnames[fn].key for fn in fullnames]

    def slot_ids_to_fullnames(self, ids: Iterable[int]) -> Iterable[str]:
        return [self._sm.slots[i].fullname for i in ids]

    def run(self, signal: Optional[Signal] = None) -> SignalResult:
        begins: List[Node]
        if signal and signal.name:
            begins = [self._signals[signal.name]]
        else:
            begins = [n for n in self._begins.values()]

        if not begins:
            raise ValueError("The begin-nodes not found")

        self._reset_states()
        if signal:
            for k, v in signal.inject_slots.items():
                box = self.get_slot(k).box
                box.set_data(v)
                box.active()

        execution_order: List[int] = list()
        for node in begins:
            execution_order += self._run_node(node)

        if signal is None:
            return SignalResult()

        return SignalResult(
            name=signal.name,
            extracted_slots=self.get_dataset(signal.extract_slots),
            execution_order=execution_order,
        )

    def send_signal(
        self,
        name: Optional[str] = None,
        inject_slots: Optional[List[BoxData]] = None,
        extract_slots: Optional[List[BoxRequest]] = None,
    ) -> List[BoxData]:
        signal = Signal(name)

        if inject_slots:
            for inject_slot in inject_slots:
                slot_key = Slot.create_key(inject_slot.node, inject_slot.slot)
                signal.inject_slots[self.get_slot(slot_key).key] = inject_slot.data

        if extract_slots:
            for extract_slot in extract_slots:
                slot_key = Slot.create_key(extract_slot.node, extract_slot.slot)
                signal.extract_slots.append(self.get_slot(slot_key).key)

        signal_result = self.run(signal)

        result = list()
        for key, data in signal_result.extracted_slots.items():
            slot = self.get_slot(key)
            node_name = slot.base_node_name
            slot_name = slot.name
            data = slot.box.data
            result.append(BoxData(node_name, slot_name, data))
        return result
