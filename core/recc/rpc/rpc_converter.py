# -*- coding: utf-8 -*-

from typing import Optional, List, Iterable, Any, Callable
from recc.vs.box import BoxData, BoxRequest
from recc.proto.api_pb2 import (
    NodeSlotPath,
    NodeSlotData,
    NodeSlotDataRequest,
)

PicklingCallable = Callable[[Any], bytes]
UnpicklingCallable = Callable[[bytes], Any]

# ------------------------
# BoxData <-> NodeSlotData
# ------------------------


def cvt_node_slot_data(obj: BoxData, cb: PicklingCallable) -> NodeSlotData:
    path = NodeSlotPath(node=obj.node, slot=obj.slot)
    return NodeSlotData(path=path, data=cb(obj.data))


def cvt_box_data(obj: NodeSlotData, cb: UnpicklingCallable) -> BoxData:
    assert hasattr(obj, "path")
    assert isinstance(obj.path, NodeSlotPath)
    assert hasattr(obj, "data")
    assert hasattr(obj.path, "node")
    assert hasattr(obj.path, "slot")
    return BoxData(obj.path.node, obj.path.slot, cb(obj.data))


def cvt_node_slot_datas(
    objs: Optional[Iterable[BoxData]],
    cb: PicklingCallable,
) -> List[NodeSlotData]:
    if not objs:
        return list()
    return [cvt_node_slot_data(obj, cb) for obj in objs]


def cvt_box_datas(
    objs: Optional[Iterable[NodeSlotData]],
    cb: UnpicklingCallable,
) -> List[BoxData]:
    if not objs:
        return list()
    return [cvt_box_data(obj, cb) for obj in objs]


# ----------------------------------
# BoxRequest <-> NodeSlotDataRequest
# ----------------------------------


def cvt_node_slot_data_request(obj: BoxRequest) -> NodeSlotDataRequest:
    path = NodeSlotPath(node=obj.node, slot=obj.slot)
    return NodeSlotDataRequest(path=path)


def cvt_box_request(obj: NodeSlotDataRequest) -> BoxRequest:
    assert hasattr(obj, "path")
    assert isinstance(obj.path, NodeSlotPath)
    assert hasattr(obj.path, "node")
    assert hasattr(obj.path, "slot")
    return BoxRequest(obj.path.node, obj.path.slot)


def cvt_node_slot_data_requests(
    objs: Optional[Iterable[BoxRequest]],
) -> List[NodeSlotDataRequest]:
    if not objs:
        return list()
    return [cvt_node_slot_data_request(obj) for obj in objs]


def cvt_box_requests(
    objs: Optional[Iterable[NodeSlotDataRequest]],
) -> List[BoxRequest]:
    if not objs:
        return list()
    return [cvt_box_request(obj) for obj in objs]
