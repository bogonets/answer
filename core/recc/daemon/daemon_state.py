# -*- coding: utf-8 -*-

from enum import Enum


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
