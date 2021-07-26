# -*- coding: utf-8 -*-

from typing import Union


class PortBindingGuest:

    __slots__ = ("port", "protocol")

    port: int
    protocol: str

    def __init__(self, port: Union[int, str], protocol: str):
        if isinstance(port, int):
            self.port = port
        else:
            self.port = int(port)
        self.protocol = protocol

    def __str__(self) -> str:
        return f"{self.port}/{self.protocol}"

    def __repr__(self):
        return f"PortBindingGuest<{self.__str__()}>"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
