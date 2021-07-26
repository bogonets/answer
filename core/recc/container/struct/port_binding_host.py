# -*- coding: utf-8 -*-

from typing import Union


class PortBindingHost:

    __slots__ = ("ip", "port")

    ip: str
    port: int

    def __init__(self, ip: str, port: Union[int, str]):
        self.ip = ip
        if isinstance(port, int):
            self.port = port
        else:
            self.port = int(port)

    def __str__(self) -> str:
        return f"{self.ip}:{self.port}"

    def __repr__(self):
        return f"PortBindingHost<{self.__str__()}>"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)
