# -*- coding: utf-8 -*-

from unittest import TestCase, main
from datetime import datetime
from typing import Any, Optional, NamedTuple, List
from dataclasses import dataclass
from enum import Enum
from recc.serialization.interface import Serializable
from recc.serialization.serialize import serialize, serialize_default


class _Test0:
    def __init__(self):
        self.name = "test0"
        self.data1 = 0
        self.data2 = 1.1
        self.data3 = [1, 2, 3, 4]
        self.data4 = {"a": 0, "b": 1.2, "c": "?"}


class _Test1(Serializable):
    def __init__(self):
        self.name = "test1"
        self.test = 1
        self._tmp = 3.14


class _Test2:
    def __init__(self):
        self.name = "test2"

    def serialize(self, version: int) -> Any:  # noqa
        return {"a": 0, "b": 1, "c": 3.14}


class _Test3:
    def __init__(self):
        self.name = "test3"
        self.test1 = _Test1()
        self.test2 = _Test2()
        self.test1_list = [_Test1(), _Test1()]
        self.test2_dict = {"a": _Test2(), "b": _Test2()}


@dataclass
class _Test4:
    test1: str
    test2: Optional[str] = None

    @property
    def test3(self):
        return 30

    def test4(self):  # noqa
        return 40


@dataclass
class _Test5:
    test1: bytes


class _Enum1(Enum):
    Value0 = 0
    Value1 = 1
    Value2 = 2


class _Test6(NamedTuple):
    shape: List[int]
    dtype: str
    buffer: bytes
    strides: List[int]


class SerializeTestCase(TestCase):
    def test_test0(self):
        test = _Test0()
        data = serialize(0, test)
        result = {
            "name": "test0",
            "data1": 0,
            "data2": 1.1,
            "data3": [1, 2, 3, 4],
            "data4": {"a": 0, "b": 1.2, "c": "?"},
        }
        self.assertEqual(result, data)

    def test_test1(self):
        test = _Test1()
        data = serialize(0, test)
        result = {"name": "test1", "test": 1}
        self.assertEqual(result, data)

    def test_test2(self):
        test = _Test2()
        data = serialize(0, test)
        result = {"a": 0, "b": 1, "c": 3.14}
        self.assertEqual(result, data)

    def test_test3(self):
        test = _Test3()
        data = serialize(0, test)
        result = {
            "name": "test3",
            "test1": {"name": "test1", "test": 1},
            "test2": {"a": 0, "b": 1, "c": 3.14},
            "test1_list": [
                {"name": "test1", "test": 1},
                {"name": "test1", "test": 1},
            ],
            "test2_dict": {
                "a": {"a": 0, "b": 1, "c": 3.14},
                "b": {"a": 0, "b": 1, "c": 3.14},
            },
        }
        self.assertEqual(result, data)

    def test_test4(self):
        test = _Test4("aa")
        data = serialize(0, test)
        result = {"test1": "aa", "test3": 30}
        self.assertEqual(result, data)

    def test_test5(self):
        test = _Test5(b"abcd")
        data = serialize(0, test)
        result = {"test1": b"abcd"}
        self.assertEqual(result, data)

    def test_test6(self):
        test = _Test6([1, 2], "uint8", b"abcd", [])
        data = serialize(0, test)
        result = [[1, 2], "uint8", b"abcd", []]
        self.assertEqual(result, data)

    def test_datetime(self):
        now = datetime.fromisoformat("2021-08-07T09:42:14.776297")
        data = serialize_default(now)
        self.assertIsInstance(data, str)
        self.assertEqual(now, datetime.fromisoformat(data))

    def test_list(self):
        data = serialize_default([1, 2, 3])
        self.assertIsInstance(data, list)
        self.assertListEqual([1, 2, 3], data)

    def test_enum(self):
        data1 = serialize_default(_Enum1.Value0)
        self.assertIsInstance(data1, int)
        self.assertEqual(0, data1)

        data2 = serialize_default([_Enum1.Value0, _Enum1.Value1, _Enum1.Value2])
        self.assertIsInstance(data2, list)
        self.assertListEqual([0, 1, 2], data2)


if __name__ == "__main__":
    main()
