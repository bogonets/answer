# -*- coding: utf-8 -*-

from typing import Optional, Dict, Any
from datetime import datetime
from recc.struct._structure import _Structure


class Task(_Structure):
    def __init__(
        self,
        uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        rpc_address: Optional[str] = None,
        auth_algorithm: Optional[str] = None,
        private_key: Optional[str] = None,
        public_key: Optional[str] = None,
        maximum_restart_count: Optional[int] = None,
        numa_memory_nodes: Optional[str] = None,
        base_image_name: Optional[str] = None,
        publish_ports: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ):
        self.uid = uid
        self.project_uid = project_uid
        self.name = name
        self.description = description
        self.extra = extra
        self.rpc_address = rpc_address
        self.auth_algorithm = auth_algorithm
        self.private_key = private_key
        self.public_key = public_key
        self.maximum_restart_count = maximum_restart_count
        self.numa_memory_nodes = numa_memory_nodes
        self.base_image_name = base_image_name
        self.publish_ports = publish_ports
        self.created_at = created_at
        self.updated_at = updated_at
        self.kwargs = kwargs
