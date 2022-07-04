# -*- coding: utf-8 -*-

from type_serialize.json import dumps

from recc.blueprint.v1.converter import bp_converter
from recc.template.manager.lamda_template_manager import LamdaTemplateManager
from recc.vs.task_graph import TaskGraph
from tester.samples.read_samples import DEFAULT_ENCODING, read_sample_json  # noqa


def create_sample_task(
    filename: str,
    encoding=DEFAULT_ENCODING,
) -> TaskGraph:
    json = read_sample_json(filename, encoding)
    graph = bp_converter(json)
    assert graph.tasks is not None
    task = next(iter(graph.tasks.values()))
    task_json = str(dumps(task), encoding="utf-8")

    result = TaskGraph()
    result.set_blueprint_json(task_json, LamdaTemplateManager())
    return result
