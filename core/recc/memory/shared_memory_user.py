# -*- coding: utf-8 -*-

from typing import Dict
from multiprocessing.shared_memory import SharedMemory


class SharedMemoryUser:
    def __init__(self, *args: str):
        self._sm_names = args
        self._sms: Dict[str, SharedMemory] = dict()

    def __enter__(self) -> Dict[str, SharedMemory]:
        for name in self._sm_names:
            self._sms[name] = SharedMemory(name=name)
        return self._sms

    def __exit__(self, exc_type, exc_value, tb):
        for sm in self._sms.values():
            sm.close()
        self._sms.clear()
