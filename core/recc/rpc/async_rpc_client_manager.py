# -*- coding: utf-8 -*-

from typing import Optional, Dict, KeysView
from recc.rpc.async_rpc_client import AsyncRpcClient
from recc.rule.naming import valid_naming, naming_task
from recc.exception.recc_error import ReccArgumentError


class AsyncRpcClientManager:

    _clients: Dict[str, AsyncRpcClient]

    def __init__(self, timeout: Optional[float] = None):
        self._clients = dict()
        self._timeout = timeout

    def keys(self) -> KeysView[str]:
        return self._clients.keys()

    def get(self, key: str) -> AsyncRpcClient:
        return self._clients[key]

    def set(self, key: str, item: AsyncRpcClient) -> None:
        self._clients[key] = item

    def remove(self, key: str) -> None:
        del self._clients[key]

    def exist(self, key: str) -> bool:
        return key in self.keys()

    async def open(self) -> None:
        pass

    async def close(self) -> None:
        for key, client in self._clients.items():
            if client.is_open():
                await client.close()

    @staticmethod
    def key(group_name: str, project_name: str, task_name: str) -> str:
        if not valid_naming(group_name):
            raise ReccArgumentError(f"Invalid group name: {group_name}")
        if not valid_naming(project_name):
            raise ReccArgumentError(f"Invalid project name: {project_name}")
        if not valid_naming(task_name):
            raise ReccArgumentError(f"Invalid task name: {task_name}")
        return naming_task(group_name, project_name, task_name)

    def get_fullpath(
        self, group_name: str, project_name: str, task_name: str
    ) -> AsyncRpcClient:
        return self.get(self.key(group_name, project_name, task_name))

    def set_fullpath(
        self, group_name: str, project_name: str, task_name: str, item: AsyncRpcClient
    ) -> None:
        self.set(self.key(group_name, project_name, task_name), item)

    def remove_fullpath(
        self, group_name: str, project_name: str, task_name: str
    ) -> None:
        self.remove(self.key(group_name, project_name, task_name))

    def exist_fullpath(
        self, group_name: str, project_name: str, task_name: str
    ) -> bool:
        return self.exist(self.key(group_name, project_name, task_name))


def create_rpc_client_manager(timeout: Optional[float] = None) -> AsyncRpcClientManager:
    return AsyncRpcClientManager(timeout)
