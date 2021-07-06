# -*- coding: utf-8 -*-

from typing import Tuple
from recc.rule.naming_base import valid_naming
from recc.rule.naming_task import naming_task, split_task_name


class TaskKey:

    group: str
    project: str
    task: str

    def __init__(self, group: str, project: str, task: str):
        if not valid_naming(group):
            raise ValueError(f"Invalid group name: {group}")
        if not valid_naming(project):
            raise ValueError(f"Invalid project name: {project}")
        if not valid_naming(task):
            raise ValueError(f"Invalid task name: {task}")

        self.group = group
        self.project = project
        self.task = task

    def to_tuple(self) -> Tuple[str, str, str]:
        return self.group, self.project, self.task

    def to_fullpath(self) -> str:
        return naming_task(self.group, self.project, self.task)

    @classmethod
    def from_fullname(cls, fullname: str) -> "TaskKey":
        group, project, task = split_task_name(fullname)
        return cls(group, project, task)

    def __str__(self) -> str:
        return self.to_fullpath()

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
