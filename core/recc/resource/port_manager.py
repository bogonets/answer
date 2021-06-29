# -*- coding: utf-8 -*-

from typing import Tuple, Set, Optional
from recc.variables.port import (
    DEFAULT_MANAGEABLE_MINIMUM_PORT_NUMBER,
    DEFAULT_MANAGEABLE_MAXIMUM_PORT_NUMBER,
)


class PortManager:

    _alloc_ports: Set[int]
    _free_ports: Set[int]
    _min_port: int
    _max_port: int

    def __init__(
        self,
        min_port=DEFAULT_MANAGEABLE_MINIMUM_PORT_NUMBER,
        max_port=DEFAULT_MANAGEABLE_MAXIMUM_PORT_NUMBER,
    ):
        self._alloc_ports = set()
        self._free_ports = set()

        self._min_port = min_port
        self._max_port = max_port

        self.reset(min_port, max_port)

    def reset(self, min_port: int, max_port: int) -> None:
        if min_port >= max_port:
            msg1 = f"The min_port(`{min_port}`)"
            msg2 = f"must be less than the max_port(`{max_port}`)."
            raise ValueError(f"{msg1} {msg2}")

        free_ports = set()

        for free_port in range(min_port, max_port + 1):
            free_ports.add(free_port)

        for alloc_port in self._alloc_ports:
            if alloc_port in free_ports:
                free_ports.remove(alloc_port)

        self._min_port = min_port
        self._max_port = max_port
        self._free_ports = free_ports

    def clear(self) -> None:
        self._alloc_ports.clear()
        self._free_ports.clear()

        for i in range(self._min_port, self._max_port + 1):
            self._free_ports.add(i)

    @property
    def min_port(self) -> int:
        return self._min_port

    @property
    def max_port(self) -> int:
        return self._max_port

    @property
    def range(self) -> Tuple[int, int]:
        return self._min_port, self._max_port

    @property
    def alloc_ports(self) -> Set[int]:
        return self._alloc_ports

    @property
    def free_ports(self) -> Set[int]:
        return self._free_ports

    def manageable_port(self, port: int) -> bool:
        return self._min_port <= port <= self._max_port

    def unmanageable_port(self, port: int) -> bool:
        return not self.manageable_port(port)

    def automatic_alloc(self) -> int:
        if not self._free_ports:
            raise EOFError("Empty free port.")

        port = self._free_ports.pop()

        try:
            if port in self._alloc_ports:
                raise ValueError(f"Already allocated port: {port}")

            self._alloc_ports.add(port)
        except ValueError:  # noqa
            self._free_ports.add(port)
            raise

        return port

    def manually_alloc(self, port: int, force=False) -> None:
        if port in self._alloc_ports:
            raise ValueError(f"Already allocated port: {port}")

        if not force and self.unmanageable_port(port):
            raise ValueError(f"Unmanageable port number: {port}")

        if port in self._free_ports:
            self._free_ports.remove(port)

        self._alloc_ports.add(port)

    def alloc(self, port: Optional[int] = None, force=False) -> int:
        if port is not None:
            self.manually_alloc(port, force)
            return port
        else:
            return self.automatic_alloc()

    def free(self, port: int, force=False) -> None:
        if port in self._free_ports:
            raise ValueError(f"Already free port: {port}")

        if port in self._alloc_ports:
            self._alloc_ports.remove(port)
        elif not force and self.unmanageable_port(port):
            raise ValueError(f"Unmanageable port number: {port}")

        if force or self.manageable_port(port):
            self._free_ports.add(port)
