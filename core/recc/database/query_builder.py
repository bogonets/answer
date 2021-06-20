# -*- coding: utf-8 -*-

from enum import Enum
from typing import Tuple, List, Any
from abc import ABCMeta, abstractmethod
from recc.exception.recc_error import ReccArgumentError, ReccOperatorError

QueryString = str
Arguments = List[Any]
BuildResult = Tuple[QueryString, Arguments]

NO_SKIP_NULL_IN_WHERE = False
"""
NULLs in the where clause are not skipped.
"""


class Operator(Enum):
    EQUAL = (0, "=")
    GREATER_THAN = (1, ">")
    LESS_THAN = (2, "<")
    GREATER_EQUAL = (3, ">=")
    LESS_EQUAL = (4, "<=")
    NOT_EQUAL = (5, "!=")
    LIKE = (6, "LIKE")

    def __init__(self, number: int, operator: str):
        self.number = number
        self.operator = operator

    @property
    def value(self) -> int:
        return self.number

    @property
    def query(self) -> str:
        return self.operator


class LogicalOperator(Enum):
    AND = (0, "AND")
    OR = (1, "OR")

    def __init__(self, number: int, operator: str):
        self.number = number
        self.operator = operator

    @property
    def value(self) -> int:
        return self.number

    @property
    def query(self) -> str:
        return self.operator


class QueryBuilderInterface(metaclass=ABCMeta):
    @abstractmethod
    def build(self, table_name: str) -> BuildResult:
        raise NotImplementedError


class QueryBuilder(QueryBuilderInterface):
    def __init__(self):
        self.arguments: List[Any] = list()
        self.values = ""
        self.wheres = ""

    @property
    def insert_index(self) -> int:
        return len(self.arguments) + 1

    def build(self, table_name: str) -> BuildResult:
        raise NotImplementedError


class WhereStatement:
    def __init__(self, base_builder: QueryBuilder):
        self._base = base_builder

    def logical(self, logical: LogicalOperator) -> "WhereStatement":
        if self._base.wheres:
            self._base.wheres += f" {logical.query} "
        return self

    @property
    def a(self) -> "WhereStatement":
        return self.logical(LogicalOperator.AND)

    @property
    def o(self) -> "WhereStatement":
        return self.logical(LogicalOperator.OR)

    def is_null(self, key: str) -> "WhereStatement":
        self._base.wheres += f"{key} IS NULL"
        return self

    def condition(self, key: str, op: Operator, value: Any) -> "WhereStatement":
        if value is None:
            if op == Operator.EQUAL:
                self._base.wheres += f"{key} IS NULL"
            else:
                msg = "If the value is None, the Operator only allows EQUAL."
                raise ReccOperatorError(msg)
        else:
            self._base.wheres += f"{key} {op.query} ${self._base.insert_index}"
            self._base.arguments.append(value)
        return self

    def _condition_by_dict(self, op: Operator, **kwargs) -> "WhereStatement":
        items = kwargs.items()
        if len(items) != 1:
            raise ReccArgumentError("Only one argument is allowed.")
        key, val = list(items)[0]
        self.condition(key, op, val)
        return self

    def eq(self, **kwargs) -> "WhereStatement":
        return self._condition_by_dict(Operator.EQUAL, **kwargs)

    def gt(self, **kwargs) -> "WhereStatement":
        return self._condition_by_dict(Operator.GREATER_THAN, **kwargs)

    def lt(self, **kwargs) -> "WhereStatement":
        return self._condition_by_dict(Operator.LESS_THAN, **kwargs)

    def ge(self, **kwargs) -> "WhereStatement":
        return self._condition_by_dict(Operator.GREATER_EQUAL, **kwargs)

    def le(self, **kwargs) -> "WhereStatement":
        return self._condition_by_dict(Operator.LESS_EQUAL, **kwargs)

    def ne(self, **kwargs) -> "WhereStatement":
        return self._condition_by_dict(Operator.NOT_EQUAL, **kwargs)

    def like(self, **kwargs) -> "WhereStatement":
        return self._condition_by_dict(Operator.LIKE, **kwargs)


class UpdateBuilder(QueryBuilder):
    def __init__(self, if_none_skip=False, **kwargs):
        super().__init__()
        if if_none_skip:
            self.multiset_if_none_skip(**kwargs)
        else:
            self.multiset(**kwargs)

    def set(self, key: str, value: Any) -> None:
        if self.values:
            self.values += ","

        if value is None:
            self.values += f"{key}=NULL"
        else:
            self.values += f"{key}=${self.insert_index}"
            self.arguments.append(value)

    def multiset(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.set(k, v)

    def multiset_if_none_skip(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if v is not None:
                self.set(k, v)

    def where(self) -> WhereStatement:
        return WhereStatement(self)

    def build(self, table_name: str) -> BuildResult:
        return (
            f"UPDATE {table_name} SET {self.values} WHERE {self.wheres};",
            self.arguments,
        )
