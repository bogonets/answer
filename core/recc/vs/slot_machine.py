# -*- coding: utf-8 -*-

from typing import Dict
from recc.vs.slot import SlotDirection, SlotCategory, Slot, SlotKey


class SlotMachine:
    def __init__(self):
        self.fullnames: Dict[str, Slot] = dict()
        self.slots: Dict[int, Slot] = dict()
        self.inputs: Dict[int, Slot] = dict()
        self.outputs: Dict[int, Slot] = dict()
        self.in_flows: Dict[int, Slot] = dict()
        self.out_flows: Dict[int, Slot] = dict()
        self.in_datas: Dict[int, Slot] = dict()
        self.out_datas: Dict[int, Slot] = dict()

    def clear(self) -> None:
        self.fullnames.clear()
        self.slots.clear()
        self.inputs.clear()
        self.outputs.clear()
        self.in_flows.clear()
        self.out_flows.clear()
        self.in_datas.clear()
        self.out_datas.clear()

    def add_in_flow(self, slot: Slot) -> None:
        assert slot.direction == SlotDirection.Input
        assert slot.category == SlotCategory.Flow
        self.fullnames[slot.fullname] = slot
        self.slots[slot.key] = slot
        self.inputs[slot.key] = slot
        self.in_flows[slot.key] = slot

    def add_out_flow(self, slot: Slot) -> None:
        assert slot.direction == SlotDirection.Output
        assert slot.category == SlotCategory.Flow
        self.fullnames[slot.fullname] = slot
        self.slots[slot.key] = slot
        self.outputs[slot.key] = slot
        self.out_flows[slot.key] = slot

    def add_in_data(self, slot: Slot) -> None:
        assert slot.direction == SlotDirection.Input
        assert slot.category == SlotCategory.Data
        self.fullnames[slot.fullname] = slot
        self.slots[slot.key] = slot
        self.inputs[slot.key] = slot
        self.in_datas[slot.key] = slot

    def add_out_data(self, slot: Slot) -> None:
        assert slot.direction == SlotDirection.Output
        assert slot.category == SlotCategory.Data
        self.fullnames[slot.fullname] = slot
        self.slots[slot.key] = slot
        self.outputs[slot.key] = slot
        self.out_datas[slot.key] = slot

    def get_slot_count(self) -> int:
        return len(self.slots)

    def get_inputs_count(self) -> int:
        return len(self.inputs)

    def get_outputs_count(self) -> int:
        return len(self.outputs)

    def get_in_flows_count(self) -> int:
        return len(self.in_flows)

    def get_out_flows_count(self) -> int:
        return len(self.out_flows)

    def get_in_datas_count(self) -> int:
        return len(self.in_datas)

    def get_out_datas_count(self) -> int:
        return len(self.out_datas)

    def get_slot(self, key: SlotKey) -> Slot:
        if isinstance(key, Slot):
            if key != self.slots[key.key]:
                raise KeyError(f"Unregistered slot object: key={key.key}")
            return key
        elif isinstance(key, int):
            return self.slots[key]
        elif isinstance(key, str):
            return self.fullnames[key]
        else:
            raise KeyError(f"Unsupported key type: {type(key).__name__}")

    def exist_slot(self, key: SlotKey) -> bool:
        try:
            self.get_slot(key)
            return True
        except KeyError:
            return False

    def remove_slot(self, key: SlotKey) -> None:
        slot = self.get_slot(key)
        uid = slot.key
        fullname = slot.fullname
        direction = slot.direction
        category = slot.category

        if direction == SlotDirection.Input and category == SlotCategory.Flow:
            del self.inputs[uid]
            del self.in_flows[uid]
        elif direction == SlotDirection.Output and category == SlotCategory.Flow:
            del self.outputs[uid]
            del self.out_flows[uid]
        elif direction == SlotDirection.Input and category == SlotCategory.Data:
            del self.inputs[uid]
            del self.in_datas[uid]
        elif direction == SlotDirection.Output and category == SlotCategory.Data:
            del self.outputs[uid]
            del self.out_datas[uid]
        else:
            raise ValueError(f"Unknown direction{direction} or category({category})")

        del self.fullnames[fullname]
        del self.slots[uid]
