# -*- coding: utf-8 -*-

from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Task:
    uid: Optional[int] = None
    project_uid: Optional[int] = None
    slug: Optional[str] = None
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
