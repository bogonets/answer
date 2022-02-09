# -*- coding: utf-8 -*-

from typing import Deque, Dict, Optional
from collections import deque
from multiprocessing.shared_memory import SharedMemory

SHARED_MEMORY_INFINITY_QUEUE = 0


def _create_shared_memory(buffer_size: int) -> SharedMemory:
    return SharedMemory(create=True, size=buffer_size)


def _destroy_shared_memory(sm: SharedMemory) -> None:
    sm.close()
    sm.unlink()


class SharedMemoryQueue:
    def __init__(self, max_queue=SHARED_MEMORY_INFINITY_QUEUE):
        self._max_queue = max_queue
        self._waiting: Deque[SharedMemory] = deque()
        self._working: Dict[str, SharedMemory] = dict()

    @property
    def max_queue(self) -> int:
        return self._max_queue

    def clear_waiting(self) -> None:
        while self._waiting:
            sm = self._waiting.popleft()
            _destroy_shared_memory(sm)
        assert not self._waiting

    def clear_working(self) -> None:
        while self._working:
            _, sm = self._working.popitem()
            _destroy_shared_memory(sm)
        assert not self._working

    def clear(self) -> None:
        self.clear_waiting()
        self.clear_working()

    def size_waiting(self) -> int:
        return len(self._waiting)

    def size_working(self) -> int:
        return len(self._working)

    def find_working(self, key: str) -> SharedMemory:
        return self._working[key]

    def secure_worker(self, size: int) -> SharedMemory:
        try:
            sm = self._waiting.popleft()
            if sm.size < size:
                _destroy_shared_memory(sm)
                raise BufferError
        except (IndexError, BufferError):
            sm = _create_shared_memory(size)
        assert sm is not None
        self._working[sm.name] = sm
        return sm

    def write(self, data: bytes, offset=0) -> str:
        buffer_size = offset + len(data)
        sm = self.secure_worker(buffer_size)
        end = offset + len(data)
        sm.buf[offset:end] = data
        return sm.name

    def restore(self, name: str) -> None:
        self._waiting.append(self._working.pop(name))

    @staticmethod
    def read(name: str, offset=0, size: Optional[int] = None) -> bytes:
        sm = SharedMemory(name=name)
        if size is None:
            return bytes(sm.buf[offset:])
        else:
            if size <= 0:
                raise ValueError("The 'size' argument must be greater than 0")
            end = offset + size
            return bytes(sm.buf[offset:end])

    class RentalManager:

        __slots__ = ("_sm", "_smq")

        def __init__(self, sm: SharedMemory, smq: "SharedMemoryQueue"):
            self._sm = sm
            self._smq = smq

        def __enter__(self) -> SharedMemory:
            return self._sm

        def __exit__(self, exc_type, exc_value, tb):
            self._smq.restore(self._sm.name)

    def rent(self, size: Optional[int] = None) -> RentalManager:
        return self.RentalManager(self.secure_worker(size), self)
