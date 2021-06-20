# -*- coding: utf-8 -*-

from typing import Dict, Optional, Any, Iterable, List


class Signal:

    name: str
    inject_slots: Dict[int, Any]
    extract_slots: List[int]

    def __init__(
        self,
        name: Optional[str] = None,
        inject_slots: Optional[Dict[int, Any]] = None,
        extract_slots: Optional[Iterable[int]] = None,
    ):
        self.name = name if name else str()
        self.inject_slots = inject_slots if inject_slots else dict()
        self.extract_slots = list(extract_slots) if extract_slots else list()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Signal[name={self.name}]"


class SignalResult:

    name: str
    extracted_slots: Dict[int, Any]
    execution_order: List[int]

    def __init__(
        self,
        name: Optional[str] = None,
        extracted_slots: Optional[Dict[int, Any]] = None,
        execution_order: Optional[Iterable[int]] = None,
    ):
        self.name = name if name else str()
        self.extracted_slots = extracted_slots if extracted_slots else dict()
        self.execution_order = list(execution_order) if execution_order else list()
