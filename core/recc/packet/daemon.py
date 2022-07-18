# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique
from typing import Optional


@dataclass
class Daemon:
    """It is mapped to the `daemon` table in the database."""

    uid: int
    plugin: str
    slug: str
    name: str
    address: str
    description: str
    enable: bool
    created_at: datetime
    updated_at: datetime


@unique
class DaemonState(Enum):
    Unknown = 0
    Unregistered = 1
    Down = 2
    NoSuchProcess = 3

    Running = 101
    Sleeping = 102
    DiskSleep = 103
    Stopped = 104
    TracingStop = 105
    Zombie = 106
    Dead = 107
    WakeKill = 108
    Waking = 109
    Idle = 110
    Locked = 111
    Waiting = 112
    Suspended = 113
    Parked = 114

    @property
    def invalid(self) -> bool:
        return self.value < 100

    @classmethod
    def from_process_status(cls, status: str):
        if status == "running":
            return cls.Running
        elif status == "sleeping":
            return cls.Sleeping
        elif status == "disk-sleep":
            return cls.DiskSleep
        elif status == "stopped":
            return cls.Stopped
        elif status == "tracing-stop":
            return cls.TracingStop
        elif status == "zombie":
            return cls.Zombie
        elif status == "dead":
            return cls.Dead
        elif status == "wake-kill":
            return cls.WakeKill
        elif status == "waking":
            return cls.Waking
        elif status == "idle":  # Linux, macOS, FreeBSD
            return cls.Idle
        elif status == "locked":  # FreeBSD
            return cls.Locked
        elif status == "waiting":  # FreeBSD
            return cls.Waiting
        elif status == "suspended":  # NetBSD
            return cls.Suspended
        elif status == "parked":  # Linux
            return cls.Parked
        else:
            return cls.Unknown


@dataclass
class DaemonA:
    plugin: str
    slug: str
    name: str
    address: str
    description: str
    enable: bool
    created_at: datetime
    updated_at: datetime

    state: DaemonState
    exit_code: Optional[int] = None


@dataclass
class CreateDaemonQ:
    plugin: str
    slug: str
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    enable: bool = False


@dataclass
class UpdateDaemonQ:
    slug: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    enable: Optional[bool] = False
