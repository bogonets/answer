# -*- coding: utf-8 -*-

from typing import Deque, Dict, Optional
from collections import deque
from multiprocessing.shared_memory import SharedMemory

SHARED_MEMORY_INFINITY_QUEUE = 0
SHARED_MEMORY_BUFFER_SIZE = 1024


def _create_shared_memory(buffer_size: int) -> SharedMemory:
    return SharedMemory(create=True, size=buffer_size)


def _destroy_shared_memory(sm: SharedMemory) -> None:
    sm.close()
    sm.unlink()


class SharedMemoryQueue:
    def __init__(
        self,
        max_queue=SHARED_MEMORY_INFINITY_QUEUE,
        buffer_size=SHARED_MEMORY_BUFFER_SIZE,
    ):
        self._max_queue = max_queue
        self._buffer_size = buffer_size
        self._waiting: Deque[SharedMemory] = deque()
        self._working: Dict[str, SharedMemory] = dict()

    @property
    def max_queue(self) -> int:
        return self._max_queue

    @property
    def buffer_size(self) -> int:
        return self._buffer_size

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

    def write(self, data: bytes, offset=0) -> str:
        if (offset + len(data)) > self._buffer_size:
            raise BufferError("The size of the buffer is small")

        try:
            sm = self._waiting.popleft()
        except IndexError:
            sm = _create_shared_memory(self._buffer_size)
        assert sm is not None

        end = offset + len(data)
        sm.buf[offset:end] = data
        self._working[sm.name] = sm
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
