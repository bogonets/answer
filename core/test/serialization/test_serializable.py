# -*- coding: utf-8 -*-

from unittest import TestCase, main
from typing import Any, Optional, get_type_hints
from recc.serialization.serializable import (
    Serializable,
    is_serialize_cls,
    is_serializable_pod_cls,
    is_serializable_pod_obj,
    normalize_strings,
)
from recc.inspect.member import get_public_members


class _Test1:
    def __init__(self, number: int = 100, name: Optional[str] = None):
        self._protected = "protected"
        self.number = number
        self.name = name


class _Test2:

    _protected: str
    test: Optional[_Test1]
    name: Optional[str]

    def __init__(self, test: Optional[_Test1] = None, name: Optional[str] = None):
        self._protected = "protected"
        self.test = test
        self.name = name


class _Test3(Serializable):

    test1: Optional[_Test1]
    test2: Optional[_Test2]
    name: Optional[str]

    def serialize(self, version: int) -> Any:
        return {"name": self.name}

    def deserialize(self, version: int, data: Any) -> None:
        self.name = data.get("name")

    @property
    def version(self) -> int:
        return 10


class SerializableTestCase(TestCase):
    def test_public_members_by_obj(self):
        obj1_names = [m[0] for m in get_public_members(_Test1())]
        self.assertEqual(2, len(obj1_names))
        self.assertIn("number", obj1_names)
        self.assertIn("name", obj1_names)
        obj2_names = [m[0] for m in get_public_members(_Test2())]
        self.assertEqual(2, len(obj2_names))
        self.assertIn("test", obj2_names)
        self.assertIn("name", obj2_names)
        obj3_names = [m[0] for m in get_public_members(_Test3())]
        self.assertEqual(1, len(obj3_names))
        self.assertEqual("version", obj3_names[0])

    def test_public_members_by_cls(self):
        cls1_names = [m[0] for m in get_public_members(_Test1)]
        self.assertEqual(0, len(cls1_names))
        cls2_names = [m[0] for m in get_public_members(_Test2)]
        self.assertEqual(0, len(cls2_names))
        cls3_names = [m[0] for m in get_public_members(_Test3)]
        self.assertEqual(1, len(cls3_names))
        self.assertEqual("version", cls3_names[0])

    def test_is_serialize_cls(self):
        self.assertFalse(is_serialize_cls(_Test1))
        self.assertFalse(is_serialize_cls(_Test2))
        self.assertTrue(is_serialize_cls(_Test3))

        self.assertFalse(is_serialize_cls(_Test1()))
        self.assertFalse(is_serialize_cls(_Test2()))
        self.assertFalse(is_serialize_cls(_Test3()))

    def test_is_serializable_pod_cls(self):
        self.assertFalse(is_serializable_pod_cls(_Test1))
        self.assertFalse(is_serializable_pod_cls(_Test2))
        self.assertFalse(is_serializable_pod_cls(_Test3))

        self.assertTrue(is_serializable_pod_cls(str))
        self.assertTrue(is_serializable_pod_cls(int))
        self.assertTrue(is_serializable_pod_cls(float))

        self.assertFalse(is_serializable_pod_cls("a"))
        self.assertFalse(is_serializable_pod_cls(100))
        self.assertFalse(is_serializable_pod_cls(3.14))

    def test_is_serializable_pod_obj(self):
        self.assertFalse(is_serializable_pod_obj(_Test1))
        self.assertFalse(is_serializable_pod_obj(_Test2))
        self.assertFalse(is_serializable_pod_obj(_Test3))

        self.assertFalse(is_serializable_pod_obj(str))
        self.assertFalse(is_serializable_pod_obj(int))
        self.assertFalse(is_serializable_pod_obj(float))

        self.assertTrue(is_serializable_pod_obj("a"))
        self.assertTrue(is_serializable_pod_obj(100))
        self.assertTrue(is_serializable_pod_obj(3.14))

    def test_get_type_hints(self):
        hint1 = get_type_hints(_Test1)
        hint2 = get_type_hints(_Test2)
        hint3 = get_type_hints(_Test3)
        self.assertEqual(0, len(hint1))
        self.assertEqual(3, len(hint2))
        self.assertEqual(3, len(hint3))

    def test_normalize_strings(self):
        self.assertIsNone(normalize_strings(None))
        self.assertEqual(["a"], normalize_strings("a"))
        self.assertEqual(["1"], normalize_strings(1))
        self.assertEqual(["9.5"], normalize_strings(9.5))
        self.assertEqual(["a", "c"], normalize_strings(["a", "c"]))
        self.assertEqual(["1", "2"], normalize_strings((1, 2)))
        self.assertEqual(["9.5", "10.1"], normalize_strings((9.5, 10.1)))
        self.assertEqual(["a", "1"], normalize_strings(["a", 1]))


if __name__ == "__main__":
    main()
