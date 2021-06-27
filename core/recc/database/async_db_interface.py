# -*- coding: utf-8 -*-

from enum import Enum
from typing import Any, Optional, List, Dict
from abc import ABCMeta, abstractmethod
from datetime import datetime
from recc.struct.group import Group
from recc.struct.group_member import GroupMember
from recc.struct.info import Info
from recc.struct.layout import Layout
from recc.struct.permission import Permission
from recc.struct.port import Port
from recc.struct.project import Project
from recc.struct.project_member import ProjectMember
from recc.struct.task import Task
from recc.struct.user import User, PassInfo
from recc.struct.widget import Widget


class PluginCategory(Enum):
    UNKNOWN = 0
    LAMBDA = 1
    WIDGET = 2


class PluginInstallType(Enum):
    UNKNOWN = 0
    LOCAL = 1
    GIT = 2


class SlotDirection(Enum):
    UNKNOWN = 0
    INPUT = 1
    OUTPUT = 2


class AsyncDatabaseInterface(metaclass=ABCMeta):
    """
    Asynchronous database interface.
    """

    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def drop(self) -> None:
        raise NotImplementedError

    # ----------------------
    # Database miscellaneous
    # ----------------------

    @abstractmethod
    async def create_tables(self, created_at=datetime.utcnow()) -> None:
        raise NotImplementedError

    @abstractmethod
    async def drop_tables(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_cache(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_anonymous_group_uid(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_guest_permission_uid(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_reporter_permission_uid(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_operator_permission_uid(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_maintainer_permission_uid(self) -> int:
        raise NotImplementedError

    # ----
    # Info
    # ----

    @abstractmethod
    async def create_info(
        self,
        key: str,
        value: str,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_info_value_by_key(
        self, key: str, value: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_info_by_key(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_info_by_key(self, key: str) -> Info:
        raise NotImplementedError

    @abstractmethod
    async def get_infos(self) -> List[Info]:
        raise NotImplementedError

    @abstractmethod
    async def get_database_version(self) -> str:
        raise NotImplementedError

    # ----
    # User
    # ----

    @abstractmethod
    async def create_user(
        self,
        username: str,
        password: str,
        salt: str,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin=False,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_last_login_by_username(
        self, username: str, last_login=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_username_by_uid(
        self, uid: int, username: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_password_and_salt_by_uid(
        self, uid: int, password: str, salt: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_password_and_salt_by_username(
        self, username: str, password: str, salt: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_extra_by_username(
        self, username: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user_by_username(
        self,
        username: str,
        email: Optional[str] = None,
        phone1: Optional[str] = None,
        phone2: Optional[str] = None,
        is_admin: Optional[bool] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_name(self, username: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_uid_by_username(self, username: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exist_user(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_user_password_and_salt(self, username: str) -> PassInfo:
        raise NotImplementedError

    @abstractmethod
    async def get_user_extra(self, username: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_users(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def exist_admin_user(self) -> bool:
        raise NotImplementedError

    # ----------
    # Permission
    # ----------

    @abstractmethod
    async def create_permission(
        self,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        r_layout=False,
        w_layout=False,
        r_storage=False,
        w_storage=False,
        r_manager=False,
        w_manager=False,
        r_graph=False,
        w_graph=False,
        r_member=False,
        w_member=False,
        r_setting=False,
        w_setting=False,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_by_uid(
        self,
        uid: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        r_layout: Optional[bool] = None,
        w_layout: Optional[bool] = None,
        r_storage: Optional[bool] = None,
        w_storage: Optional[bool] = None,
        r_manager: Optional[bool] = None,
        w_manager: Optional[bool] = None,
        r_graph: Optional[bool] = None,
        w_graph: Optional[bool] = None,
        r_member: Optional[bool] = None,
        w_member: Optional[bool] = None,
        r_setting: Optional[bool] = None,
        w_setting: Optional[bool] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_description_by_name(
        self, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_permission_extra_by_name(
        self, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_permission_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_permission_by_name(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_permission_by_uid(self, uid: int) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def get_permission_by_name(self, name: str) -> Permission:
        raise NotImplementedError

    @abstractmethod
    async def get_permissions(self) -> List[Permission]:
        raise NotImplementedError

    @abstractmethod
    async def get_project_permission_by_uid(
        self, user_uid: int, project_uid: int
    ) -> Permission:
        raise NotImplementedError

    # -----
    # Group
    # -----

    @abstractmethod
    async def create_group(
        self,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_description_by_name(
        self, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_extra_by_name(
        self, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_by_name(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_group_by_uid(self, uid: int) -> Group:
        raise NotImplementedError

    @abstractmethod
    async def get_group_by_name(self, name: str) -> Group:
        raise NotImplementedError

    @abstractmethod
    async def get_groups(self) -> List[Group]:
        raise NotImplementedError

    # ------------
    # Group member
    # ------------

    @abstractmethod
    async def create_group_member(
        self, group_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_group_member_permission(
        self, group_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_group_member(self, group_uid: int, user_uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_group_member(self, group_uid: int, user_uid: int) -> GroupMember:
        raise NotImplementedError

    @abstractmethod
    async def get_group_member_by_group_uid(self, group_uid: int) -> List[GroupMember]:
        raise NotImplementedError

    @abstractmethod
    async def get_group_member_by_user_uid(self, user_uid: int) -> List[GroupMember]:
        raise NotImplementedError

    @abstractmethod
    async def get_group_members(self) -> List[GroupMember]:
        raise NotImplementedError

    # -------
    # Project
    # -------

    @abstractmethod
    async def create_project(
        self,
        group_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_description_by_name(
        self, group_uid: int, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_extra_by_name(
        self, group_uid: int, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_project_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_project_by_name(self, group_uid: int, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_uid(self, uid: int) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_name(self, group_uid: int, name: str) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_group_uid(self, group_uid: int) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    async def get_project_by_fullpath(
        self, group_name: str, project_name: str
    ) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def get_project_uid_by_fullpath(
        self, group_name: str, project_name: str
    ) -> int:
        raise NotImplementedError

    # --------------
    # Project member
    # --------------

    @abstractmethod
    async def create_project_member(
        self, project_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_project_member_permission(
        self, project_uid: int, user_uid: int, permission_uid: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_project_member(self, project_uid: int, user_uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_project_member(
        self, project_uid: int, user_uid: int
    ) -> ProjectMember:
        raise NotImplementedError

    @abstractmethod
    async def get_project_member_by_project_uid(
        self, project_uid: int
    ) -> List[ProjectMember]:
        raise NotImplementedError

    @abstractmethod
    async def get_project_member_by_user_uid(
        self, user_uid: int
    ) -> List[ProjectMember]:
        raise NotImplementedError

    @abstractmethod
    async def get_project_members(self) -> List[ProjectMember]:
        raise NotImplementedError

    # ----
    # Task
    # ----

    @abstractmethod
    async def create_task(
        self,
        project_uid: int,
        name: str,
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
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_description_by_name(
        self,
        project_uid: int,
        name: str,
        description: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_extra_by_name(
        self, project_uid: int, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_keys_by_uid(
        self,
        uid: int,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_keys_by_name(
        self,
        project_uid: int,
        name: str,
        auth_algorithm: str,
        private_key: str,
        public_key: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task_by_uid(
        self,
        uid: int,
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
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_task_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_task_by_name(self, project_uid: int, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_uid(self, uid: int) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_name(self, project_uid: int, name: str) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def get_task_uid_by_name(self, project_uid: int, name: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_project_uid(self, project_uid: int) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_fullpath(
        self, group_name: str, project_name: str, task_name: str
    ) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def get_task_uid_by_fullpath(
        self, group_name: str, project_name: str, task_name: str
    ) -> int:
        raise NotImplementedError

    # ------
    # Layout
    # ------

    @abstractmethod
    async def create_layout(
        self,
        project_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_layout_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_layout_description_by_name(
        self,
        project_uid: int,
        name: str,
        description: str,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_layout_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_layout_extra_by_name(
        self, project_uid: int, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_layout_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_layout_by_name(self, project_uid: int, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_layout_by_uid(self, uid: int) -> Layout:
        raise NotImplementedError

    @abstractmethod
    async def get_layout_by_name(self, project_uid: int, name: str) -> Layout:
        raise NotImplementedError

    @abstractmethod
    async def get_layout_by_project_uid(self, project_uid: int) -> List[Layout]:
        raise NotImplementedError

    # ------
    # Widget
    # ------

    @abstractmethod
    async def create_widget(
        self,
        layout_uid: int,
        name: str,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_widget_description_by_uid(
        self, uid: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_widget_description_by_name(
        self, layout_uid: int, name: str, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_widget_extra_by_uid(
        self, uid: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_widget_extra_by_name(
        self, layout_uid: int, name: str, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_widget_by_uid(self, uid: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_widget_by_name(self, layout_uid: int, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_widget_by_uid(self, uid: int) -> Widget:
        raise NotImplementedError

    @abstractmethod
    async def get_widget_by_name(self, layout_uid: int, name: str) -> Widget:
        raise NotImplementedError

    @abstractmethod
    async def get_widget_by_layout_uid(self, layout_uid: int) -> List[Widget]:
        raise NotImplementedError

    # ----
    # Port
    # ----

    @abstractmethod
    async def create_port(
        self,
        number: int,
        group_uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        task_uid: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        created_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_description_by_number(
        self, number: int, description: str, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_extra_by_number(
        self, number: int, extra: Any, updated_at=datetime.utcnow()
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_port_by_number(
        self,
        number: int,
        group_uid: Optional[int] = None,
        project_uid: Optional[int] = None,
        task_uid: Optional[int] = None,
        description: Optional[str] = None,
        extra: Optional[Any] = None,
        updated_at=datetime.utcnow(),
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_port_by_number(self, number: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_port_by_number(self, number: int) -> Port:
        raise NotImplementedError

    @abstractmethod
    async def get_port_by_group_uid(self, group_uid: int) -> List[Port]:
        raise NotImplementedError

    @abstractmethod
    async def get_port_by_project_uid(self, project_uid: int) -> List[Port]:
        raise NotImplementedError

    @abstractmethod
    async def get_port_by_task_uid(self, task_uid: int) -> List[Port]:
        raise NotImplementedError

    @abstractmethod
    async def get_ports(self) -> List[Port]:
        raise NotImplementedError
