# -*- coding: utf-8 -*-

import numpy as np
from unittest import TestCase, main
from recc.numpy.numpy_proto import NumpyProto


class NumpyProtoTestCase(TestCase):
    def test_default(self):
        array0 = np.random.randint(0, 255, size=(10, 20), dtype=np.int16)

        proto0 = NumpyProto.from_array(array0)
        self.assertEqual(proto0.dtype_name, "int16")
        self.assertListEqual(list(proto0.shape), [10, 20])

        array1 = proto0.to_array()
        self.assertTrue((array0 == array1).all())
        self.assertEqual(array0.dtype, array1.dtype)
        self.assertTupleEqual(array0.strides, array1.strides)


if __name__ == "__main__":
    main()
