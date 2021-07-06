# -*- coding: utf-8 -*-

import numpy as np


def on_run(array: np.ndarray, index: np.ndarray):
    return {"result": np.array([array.item(*index.tolist())], dtype=array.dtype)}
