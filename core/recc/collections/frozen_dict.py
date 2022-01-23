# -*- coding: utf-8 -*-

from typing import TypeVar, Dict
from collections.abc import Mapping

KT = TypeVar("KT")
VT = TypeVar("VT")


class FrozenDict(Mapping[KT, VT]):
    def __init__(self, *args, **kwargs):
        self._dict: Dict[KT, VT] = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return self._dict.__iter__()

    def __len__(self):
        return self._dict.__len__()

    def __getitem__(self, item):
        return self._dict.__getitem__(item)

    def __contains__(self, item):
        return self._dict.__contains__(item)

    def __eq__(self, other):
        return self._dict.__eq__(other)

    def __ne__(self, other):
        return self._dict.__ne__(other)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

    def get(self, key):
        return self._dict.get(key)
