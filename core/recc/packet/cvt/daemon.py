# -*- coding: utf-8 -*-

from recc.packet.daemon import DaemonA
from recc.database.struct.daemon import Daemon


def daemon_to_answer(daemon: Daemon) -> DaemonA:
    return DaemonA(
        plugin=daemon.plugin if daemon.plugin else str(),
        slug=daemon.slug if daemon.slug else str(),
        name=daemon.name,
        address=daemon.address,
        description=daemon.description,
        enable=True if daemon.enable else False,
        created_at=daemon.created_at,
        updated_at=daemon.updated_at,
    )
