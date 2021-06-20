# -*- coding: utf-8 -*-

from tester._samples.read_samples import DEFAULT_ENCODING, read_sample_json  # noqa
from recc.vs.task import Task
from recc.blueprint.v1.converter import bp_converter
from recc.serializable.json import serialize_json_text
from recc.template.template_manager import TemplateManager


def create_sample_task(filename: str, encoding=DEFAULT_ENCODING, version=1) -> Task:
    json = read_sample_json(filename, encoding)
    graph = bp_converter(json)
    task = next(iter(graph.tasks.values()))
    task_json = serialize_json_text(version, task)

    result = Task()
    result.set_blueprint_json(task_json, version, TemplateManager())
    return result
