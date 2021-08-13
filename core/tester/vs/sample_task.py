# -*- coding: utf-8 -*-

from tester.samples.read_samples import DEFAULT_ENCODING, read_sample_json  # noqa
from recc.vs.task_graph import TaskGraph
from recc.blueprint.v1.converter import bp_converter
from recc.serialization.json import serialize_json_text
from recc.template.manager.lamda_template_manager import LamdaTemplateManager


def create_sample_task(filename: str, encoding=DEFAULT_ENCODING, version=1) -> TaskGraph:
    json = read_sample_json(filename, encoding)
    graph = bp_converter(json)
    task = next(iter(graph.tasks.values()))
    task_json = serialize_json_text(version, task)

    result = TaskGraph()
    result.set_blueprint_json(task_json, version, LamdaTemplateManager())
    return result
