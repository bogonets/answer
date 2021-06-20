# -*- coding: utf-8 -*-

from typing import Dict, Any, List, Set
from recc.exception.recc_error import ReccNotFoundError, ReccArgumentError
from recc.blueprint.blueprint import BpSlot, BpArc, BpProperty, BpNode, BpTask, BpGraph

k_id = "id"
k_info = "info"
k_inputs = "inputs"
k_link = "link"
k_links = "links"
k_name = "name"
k_category = "category"
k_nodes = "nodes"
k_origin_id = "origin_id"
k_outputs = "outputs"
k_properties = "properties"
k_target_id = "target_id"
k_tasks = "tasks"
k_title = "title"
k_uid = "uid"
k_value = "value"


def _create_bp_props(props: Dict[int, dict]) -> Dict[str, BpProperty]:
    result: Dict[str, BpProperty] = dict()
    for prop in props:
        assert isinstance(prop, dict)
        if k_value in prop:
            bp_prop = BpProperty()
            bp_prop.value = prop[k_value]
            result[str(prop[k_name])] = bp_prop
    return result


def _create_bp_nodes(ids: List[int], nodes: Dict[int, dict]) -> Dict[str, BpNode]:
    result = dict()
    for node in [nodes[i] for i in ids]:
        bp_node = BpNode()
        bp_node.template_category = node[k_info][k_category]
        bp_node.template_name = node[k_info][k_name]
        bp_props = _create_bp_props(node[k_properties])
        if bp_props:
            bp_node.properties = bp_props
        result[str(node[k_uid])] = bp_node
    return result


def _find_input_name(link_id: int, controls: List[Dict[str, Any]]) -> str:
    for control in controls:
        if link_id == control[k_link]:
            return control[k_name]
    raise ReccNotFoundError(f"Link(`{link_id}`) is not founded.")


def _find_output_name(link_id: int, controls: List[Dict[str, Any]]) -> str:
    for control in controls:
        links = control[k_links]
        assert isinstance(links, list)
        if link_id in links:
            return control[k_name]
    raise ReccNotFoundError(f"Link(`{link_id}`) is not founded.")


def _create_bp_arcs(
    ids: List[int], links: Dict[int, dict], nodes: Dict[int, dict]
) -> Dict[str, BpArc]:
    result = dict()
    for link_id, link in [(i, links[i]) for i in ids]:
        origin_id = link[k_origin_id]
        target_id = link[k_target_id]
        assert isinstance(origin_id, int)
        assert isinstance(target_id, int)
        origin_node = nodes[origin_id]
        target_node = nodes[target_id]

        back_name = _find_output_name(link_id, origin_node[k_outputs])
        front_name = _find_input_name(link_id, target_node[k_inputs])

        bp_arc = BpArc()
        bp_arc.back = BpSlot()
        bp_arc.back.node = origin_node[k_uid]
        bp_arc.back.slot = back_name
        bp_arc.front = BpSlot()
        bp_arc.front.node = target_node[k_uid]
        bp_arc.front.slot = front_name
        result[str(link[k_id])] = bp_arc
    return result


def _find_link_ids(ids: List[int], nodes: Dict[int, dict]) -> Set[int]:
    result = set()
    for node in [nodes[i] for i in ids]:

        if k_inputs in node:
            inputs = node[k_inputs]
            assert isinstance(inputs, list)
            for i in inputs:
                assert isinstance(i, dict)
                if k_link in i and i[k_link] is not None:
                    result.add(int(i[k_link]))

        if k_outputs in node:
            outputs = node[k_outputs]
            assert isinstance(outputs, list)
            for o in outputs:
                assert isinstance(o, dict)
                if k_links in o and o[k_links] is not None:
                    for link_id in o[k_links]:
                        result.add(int(link_id))

    return result


def _create_bp_tasks(
    links: Dict[int, dict], nodes: Dict[int, dict], tasks: Dict[int, dict]
) -> Dict[str, BpTask]:
    result = dict()
    for task_id, task in tasks.items():
        bp_task = BpTask()

        task_node_ids = task[k_nodes]
        assert isinstance(task_node_ids, list)
        bp_nodes = _create_bp_nodes(task_node_ids, nodes)
        if bp_nodes:
            bp_task.nodes = bp_nodes

        link_ids = _find_link_ids(task_node_ids, nodes)
        if link_ids:
            bp_arcs = _create_bp_arcs(list(link_ids), links, nodes)
            if bp_arcs:
                bp_task.arcs = bp_arcs
        result[str(task[k_title])] = bp_task
    return result


def _create_bp_graph(data: Dict[str, Any]) -> BpGraph:
    _links = data[k_links]
    _nodes = data[k_nodes]
    _tasks = data[k_tasks]

    if not isinstance(_links, list):
        raise ReccArgumentError("data['links'] must be of type `list`.")
    if not isinstance(_nodes, list):
        raise ReccArgumentError("data['nodes'] must be of type `list`.")
    if not isinstance(_tasks, list):
        raise ReccArgumentError("data['tasks'] must be of type `list`.")

    links: Dict[int, dict] = {link[k_id]: link for link in _links}
    nodes: Dict[int, dict] = {node[k_id]: node for node in _nodes}
    tasks: Dict[int, dict] = {task[k_id]: task for task in _tasks}

    result = BpGraph()
    result.tasks = _create_bp_tasks(links, nodes, tasks)
    return result


def bp_converter(data: Dict[str, Any]) -> BpGraph:
    return _create_bp_graph(data)
