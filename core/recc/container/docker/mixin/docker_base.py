# -*- coding: utf-8 -*-

from typing import Optional
from docker import DockerClient


class DockerBase:

    _host: str
    _port: Optional[int]
    _docker: Optional[DockerClient]

    @property
    def base_url(self):
        if self._port:
            return f"{self._host}:{self._port}"
        else:
            return self._host

    @property
    def docker(self) -> DockerClient:
        assert self._docker is not None
        return self._docker
