# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Task:
    """It is mapped to the `task` table in the database."""

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
