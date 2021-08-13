# -*- coding: utf-8 -*-

from unittest import TestCase, main
from datetime import datetime
from typing import Any, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from recc.serialization.serializable import DeserializeInterface
from recc.serialization.deserialize import deserialize, deserialize_default


class _Test0:
    def __init__(self):
        pass


class _Test1:
    a: int
    b: float
    c: str

    def __init__(self):
        pass


class _Test2:
    name: str
    data1: _Test1
    data2: List[_Test1]
    data3: Dict[str, _Test1]

    def __init__(self):
        pass


class _Test3(DeserializeInterface):
    def __init__(self):
        self.version = None
        self.data = None

    def deserialize(self, version: int, data: Any) -> None:
        self.version = version
        self.data = data


class _Test4:
    def __init__(self):
        self.test1 = None
        self.test2 = None
        self.test3 = None

    def deserialize(self, version: int, data: Any) -> None:  # noqa
        self.test1 = deserialize(version, data.get("test1"), _Test1)
        self.test2 = deserialize(version, data.get("test2"), _Test2)
        self.test3 = deserialize(version, data.get("test3"), _Test3)


class _Test5:
    data1: Optional[_Test1]
    data2: Any

    def __init__(self):
        pass


class _Test6:
    data1: List[int]
    data2: List[_Test1]
    data3: Dict[str, int]
    data4: Optional[Dict[str, int]]

    def __init__(self):
        pass


@dataclass
class _Test7:
    test1: str
    test2: Optional[str] = None


class _Enum1(Enum):
    Value0 = 0
    Value1 = 1
    Value2 = 2


class DeserializeTestCase(TestCase):
    def test_test0(self):
        result = deserialize(0, {"E": 100, "W": 3.14, "Q": "?"}, _Test0)
        self.assertIsInstance(result, _Test0)
        self.assertEqual(100, getattr(result, "E"))
        self.assertEqual(3.14, getattr(result, "W"))
        self.assertEqual("?", getattr(result, "Q"))

    def test_test1(self):
        result = deserialize(0, {"a": 100, "b": 3.14, "c": "?"}, _Test1)
        self.assertIsInstance(result, _Test1)
        self.assertEqual(100, result.a)
        self.assertEqual(3.14, result.b)
        self.assertEqual("?", result.c)

    def test_test2_1(self):
        data = {
            "name": "test2",
            "data1": {"a": 100, "b": 3.14, "c": "?"},
            "data2": [{"a": 2}, {"b": 0.1}, {"c": "/"}],
            "data3": {"AA": {"a": 200}, "BB": {"b": 9.1}, "CC": {"c": "M"}},
        }
        result = deserialize(0, data, _Test2)
        self.assertIsInstance(result, _Test2)
        self.assertEqual("test2", result.name)
        self.assertEqual(100, result.data1.a)
        self.assertEqual(3.14, result.data1.b)
        self.assertEqual("?", result.data1.c)
        self.assertIsInstance(result.data2, list)
        self.assertEqual(3, len(result.data2))
        self.assertEqual(2, result.data2[0].a)
        self.assertEqual(0.1, result.data2[1].b)
        self.assertEqual("/", result.data2[2].c)
        self.assertIsInstance(result.data3, dict)
        self.assertEqual(200, result.data3["AA"].a)
        self.assertEqual(9.1, result.data3["BB"].b)
        self.assertEqual("M", result.data3["CC"].c)

    def test_test3(self):
        result = deserialize(0, {"a": 10}, _Test3)
        self.assertIsInstance(result, _Test3)
        self.assertEqual(0, result.version)
        self.assertEqual({"a": 10}, result.data)

    def test_test4(self):
        data = {
            "test1": {"a": 100, "b": 3.14, "c": "?"},
            "test2": {
                "name": "test2",
                "data1": {"a": 100, "b": 3.14, "c": "?"},
                "data2": [{"a": 2}, {"b": 0.1}, {"c": "/"}],
                "data3": {"AA": {"a": 200}, "BB": {"b": 9.1}, "CC": {"c": "M"}},
            },
            "test3": ["hello", "world", "!!"],
            "test4": "skip",
        }
        result = deserialize(0, data, _Test4)
        self.assertIsInstance(result, _Test4)
        test1 = getattr(result, "test1", None)
        test2 = getattr(result, "test2", None)
        test3 = getattr(result, "test3", None)
        self.assertIsNone(getattr(result, "test4", None))

        self.assertIsInstance(test1, _Test1)
        self.assertEqual(100, test1.a)
        self.assertEqual(3.14, test1.b)
        self.assertEqual("?", test1.c)

        self.assertIsInstance(test2, _Test2)
        self.assertEqual("test2", test2.name)
        self.assertEqual(100, test2.data1.a)
        self.assertEqual(3.14, test2.data1.b)
        self.assertEqual("?", test2.data1.c)
        self.assertIsInstance(test2.data2, list)
        self.assertEqual(3, len(test2.data2))
        self.assertEqual(2, test2.data2[0].a)
        self.assertEqual(0.1, test2.data2[1].b)
        self.assertEqual("/", test2.data2[2].c)
        self.assertIsInstance(test2.data3, dict)
        self.assertEqual(200, test2.data3["AA"].a)
        self.assertEqual(9.1, test2.data3["BB"].b)
        self.assertEqual("M", test2.data3["CC"].c)

        self.assertIsInstance(test3, _Test3)
        self.assertEqual(["hello", "world", "!!"], test3.data)

    def test_test5_1(self):
        data = {
            "data1": {"a": 100, "b": 3.14, "c": "?"},
            "data2": [{"a": 1, "b": 2}],
            "data3": 100,
        }
        result = deserialize(0, data, _Test5)
        self.assertIsInstance(result, _Test5)

        test1 = result.data1
        self.assertIsInstance(test1, _Test1)
        self.assertEqual(100, test1.a)
        self.assertEqual(3.14, test1.b)
        self.assertEqual("?", test1.c)

        self.assertEqual([{"a": 1, "b": 2}], result.data2)
        self.assertEqual(100, getattr(result, "data3", None))

    def test_test5_2(self):
        data = {
            "data1": None,
            "data3": 100,
        }
        result = deserialize(0, data, _Test5)
        self.assertIsInstance(result, _Test5)
        self.assertIsNone(getattr(result, "data1", None))
        self.assertIsNone(getattr(result, "data2", None))
        self.assertEqual(100, getattr(result, "data3", None))

    def test_test5_3(self):
        result = deserialize(0, dict(), _Test5)
        self.assertIsInstance(result, _Test5)
        self.assertIsNone(getattr(result, "data1", None))
        self.assertIsNone(getattr(result, "data2", None))
        self.assertIsNone(getattr(result, "data3", None))

    def test_test6_data1(self):
        data = {"data1": 2}
        result = deserialize(0, data, _Test6)
        self.assertIsInstance(result, _Test6)
        self.assertEqual(1, len(result.data1))
        self.assertEqual(2, result.data1[0])

    def test_test6_data2(self):
        data = {"data2": {"a": 2}}
        result = deserialize(0, data, _Test6)
        self.assertIsInstance(result, _Test6)
        self.assertEqual(1, len(result.data2))
        self.assertEqual(2, result.data2[0].a)

    def test_test6_data3(self):
        data = {"data3": [10, 20, 30]}
        result = deserialize(0, data, _Test6)
        self.assertIsInstance(result, _Test6)
        self.assertEqual(3, len(result.data3))
        self.assertEqual(10, result.data3["0"])
        self.assertEqual(20, result.data3["1"])
        self.assertEqual(30, result.data3["2"])

    def test_test6_data4(self):
        data = {"data4": 10}
        result = deserialize(0, data, _Test6)
        self.assertIsInstance(result, _Test6)
        self.assertEqual(1, len(result.data4))
        self.assertEqual(10, result.data4["0"])

    def test_manual_types(self):
        data = [{"a": 2}]
        result = deserialize(0, data, list, Optional[List[_Test1]])
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual(2, result[0].a)

    def test_test7(self):
        result = deserialize_default({"test1": "aa"}, _Test7)
        self.assertIsInstance(result, _Test7)

    def test_test7_list(self):
        result = deserialize_default([{"test1": "aa"}], List[_Test7])
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertIsInstance(result[0], _Test7)
        self.assertEqual("aa", result[0].test1)
        self.assertIsNone(result[0].test2)

    def test_test7_dict(self):
        result = deserialize_default({"key1": {"test1": "aa"}}, Dict[str, _Test7])
        self.assertIsInstance(result, dict)
        self.assertEqual(1, len(result))
        self.assertIn("key1", result)
        self.assertIsInstance(result["key1"], _Test7)
        self.assertEqual("aa", result["key1"].test1)
        self.assertIsNone(result["key1"].test2)

    def test_datetime(self):
        time_format = "2021-08-07T09:42:14.776297"
        result = deserialize_default(time_format, datetime)
        self.assertIsInstance(result, datetime)
        self.assertEqual(result, datetime.fromisoformat(time_format))

    def test_list(self):
        result = deserialize_default([1, 2, 3], list)
        self.assertIsInstance(result, list)
        self.assertListEqual(result, [1, 2, 3])

    def test_enum(self):
        result = deserialize_default([0, 1, 2], List[_Enum1])
        self.assertIsInstance(result, list)
        self.assertEqual(3, len(result))
        self.assertIsInstance(result[0], _Enum1)
        self.assertIsInstance(result[1], _Enum1)
        self.assertIsInstance(result[2], _Enum1)
        self.assertEqual(result[0], _Enum1.Value0)
        self.assertEqual(result[1], _Enum1.Value1)
        self.assertEqual(result[2], _Enum1.Value2)


if __name__ == "__main__":
    main()
