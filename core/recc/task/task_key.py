# -*- coding: utf-8 -*-

from typing import Tuple
from recc.rule.naming import valid_naming, naming_task


def make_task_key(group: str, project: str, task: str) -> str:
    if not valid_naming(group):
        raise ValueError(f"Invalid group name: {group}")
    if not valid_naming(project):
        raise ValueError(f"Invalid project name: {project}")
    if not valid_naming(task):
        raise ValueError(f"Invalid task name: {task}")
    return naming_task(group, project, task)


class TaskKey:

    group: str
    project: str
    task: str

    def __init__(self, group: str, project: str, task: str):
        self.group = group
        self.project = project
        self.task = task

    def to_tuple(self) -> Tuple[str, str, str]:
        return self.group, self.project, self.task

    def __str__(self) -> str:
        return make_task_key(self.group, self.project, self.task)

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
