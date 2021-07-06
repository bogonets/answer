# -*- coding: utf-8 -*-

from typing import Optional, Dict, KeysView
from recc.rpc.rpc_client import RpcClient
from recc.task.task_key import TaskKey


class TaskConnectionPool:

    _clients: Dict[TaskKey, RpcClient]
    _timeout: float

    def __init__(self, timeout: Optional[float] = None):
        self._clients = dict()
        self._timeout = timeout if timeout else 1.0

    @property
    def clients(self) -> Dict[TaskKey, RpcClient]:
        return self._clients

    @property
    def timeout(self) -> float:
        return self._timeout

    @staticmethod
    def make_key(group: str, project: str, task: str) -> TaskKey:
        return TaskKey(group, project, task)

    @staticmethod
    def make_key_by_fullpath(fullpath: str) -> TaskKey:
        return TaskKey.from_fullname(fullpath)

    def keys(self) -> KeysView[TaskKey]:
        return self._clients.keys()

    def get(self, key: TaskKey) -> RpcClient:
        return self._clients[key]

    def get_by_fullpath(self, fullpath: str) -> RpcClient:
        return self.get(TaskKey.from_fullname(fullpath))

    def get_by_category(self, group: str, project: str, task: str) -> RpcClient:
        return self.get(TaskKey(group, project, task))

    def __getitem__(self, item):
        return self.get(item)

    def set(self, key: TaskKey, client: RpcClient) -> None:
        self._clients[key] = client

    def set_by_fullpath(self, fullpath: str, client: RpcClient) -> None:
        return self.set(TaskKey.from_fullname(fullpath), client)

    def set_by_category(
        self, group: str, project: str, task: str, client: RpcClient
    ) -> None:
        return self.set(TaskKey(group, project, task), client)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def remove(self, key: TaskKey) -> None:
        del self._clients[key]

    def remove_by_fullpath(self, fullpath: str) -> None:
        self.remove(TaskKey.from_fullname(fullpath))

    def remove_by_category(self, group: str, project: str, task: str) -> None:
        self.remove(TaskKey(group, project, task))

    def __delitem__(self, key):
        return self.remove(key)

    def exist(self, key: TaskKey) -> bool:
        return key in self.keys()

    def exist_by_fullpath(self, fullpath: str) -> bool:
        return self.exist(TaskKey.from_fullname(fullpath))

    def exist_by_category(self, group: str, project: str, task: str) -> bool:
        return self.exist(TaskKey(group, project, task))

    def __contains__(self, item):
        return self.exist(item)

    def __len__(self):
        return len(self._clients)

    async def open(self) -> None:
        pass

    async def close(self) -> None:
        for key, client in self._clients.items():
            if client.is_open():
                await client.close()


def create_task_connection_pool(timeout: Optional[float] = None) -> TaskConnectionPool:
    return TaskConnectionPool(timeout)
