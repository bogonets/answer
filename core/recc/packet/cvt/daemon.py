# -*- coding: utf-8 -*-

from typing import Optional

from recc.daemon.daemon_state import DaemonState
from recc.database.struct.daemon import Daemon
from recc.packet.daemon import DaemonA


def daemon_to_answer(
    daemon: Daemon,
    state: DaemonState,
    exit_code: Optional[int] = None,
) -> DaemonA:
    return DaemonA(
        plugin=daemon.plugin,
        slug=daemon.slug,
        name=daemon.name,
        address=daemon.address,
        description=daemon.description,
        enable=daemon.enable,
        created_at=daemon.created_at,
        updated_at=daemon.updated_at,
        state=state,
        exit_code=exit_code,
    )
