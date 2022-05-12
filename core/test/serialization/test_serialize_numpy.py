# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional
from unittest import TestCase, main

import numpy as np

from recc.serialization.deserialize import deserialize_default
from recc.serialization.numpy import numpy_deserialize, numpy_serialize
from recc.serialization.serialize import serialize_default


@dataclass
class _Test1:
    test1: str
    test2: Optional[List[np.ndarray]] = None


class SerializeNumpyTestCase(TestCase):
    def test_numpy_serialize(self):
        image = np.random.randint(0, 255, size=(1270, 1920, 3), dtype=np.uint8)
        self.assertEqual((1270, 1920, 3), image.shape)
        self.assertEqual(np.uint8, image.dtype)
        proto = numpy_serialize(image)
        result = numpy_deserialize(proto)
        self.assertTrue((result == image).all())

    def test_numpy_serialize_tuple(self):
        image = np.random.randint(0, 255, size=(1270, 1920, 3), dtype=np.uint8)
        self.assertEqual((1270, 1920, 3), image.shape)
        self.assertEqual(np.uint8, image.dtype)
        proto = numpy_serialize(image)
        result = numpy_deserialize(tuple(proto))
        self.assertTrue((result == image).all())

    def test_default(self):
        array0 = np.random.rand(10, 20, 30)
        array1 = np.random.randint(0, 255, size=(1270, 1920, 3), dtype=np.uint8)
        test_data = _Test1("test1", [array0, array1])

        encoded_data = serialize_default(test_data)

        result_data = deserialize_default(encoded_data, _Test1)
        self.assertEqual(test_data.test1, result_data.test1)
        self.assertEqual(len(test_data.test2), len(result_data.test2))
        self.assertTrue((test_data.test2[0] == result_data.test2[0]).all())
        self.assertTrue((test_data.test2[1] == result_data.test2[1]).all())
        self.assertEqual(test_data.test2[0].dtype, result_data.test2[0].dtype)
        self.assertEqual(test_data.test2[1].dtype, result_data.test2[1].dtype)


if __name__ == "__main__":
    main()
