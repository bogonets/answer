# -*- coding: utf-8 -*-

from typing import Optional, Dict, Any, Final
from datetime import datetime
from dataclasses import dataclass
from recc.inspect.lexicographical_members import lexicographical_members


@dataclass
class Task:
    uid: Optional[int] = None
    project_uid: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    rpc_address: Optional[str] = None
    auth_algorithm: Optional[str] = None
    private_key: Optional[str] = None
    public_key: Optional[str] = None
    maximum_restart_count: Optional[int] = None
    numa_memory_nodes: Optional[str] = None
    base_image_name: Optional[str] = None
    publish_ports: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def remove_sensitive(self):
        self.uid = None


class TaskKeys:
    uid = "uid"
    project_uid = "project_uid"
    name = "name"
    description = "description"
    extra = "extra"
    rpc_address = "rpc_address"
    auth_algorithm = "auth_algorithm"
    private_key = "private_key"
    public_key = "public_key"
    maximum_restart_count = "maximum_restart_count"
    numa_memory_nodes = "numa_memory_nodes"
    base_image_name = "base_image_name"
    publish_ports = "publish_ports"
    created_at = "created_at"
    updated_at = "updated_at"


keys: Final[TaskKeys] = TaskKeys()
assert lexicographical_members(keys, Task())
