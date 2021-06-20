# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict


class BpProperty:

    value: Optional[Any] = None


class BpNode:

    template_category: Optional[str] = None
    template_name: Optional[str] = None
    properties: Optional[Dict[str, BpProperty]] = None


class BpSlot:

    node: Optional[str] = None
    slot: Optional[str] = None


class BpArc:

    back: Optional[BpSlot] = None
    front: Optional[BpSlot] = None


class BpTask:

    nodes: Optional[Dict[str, BpNode]] = None
    arcs: Optional[Dict[str, BpArc]] = None


class BpGraph:

    tasks: Optional[Dict[str, BpTask]] = None
