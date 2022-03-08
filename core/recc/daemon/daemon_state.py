# -*- coding: utf-8 -*-

from enum import Enum


class DaemonState(Enum):
    Unknown = 0
    EnvNotFound = 1
    EnvCreating = 2
    Down = 3

    Running = 4
    Sleeping = 5
    DiskSleep = 6
    Stopped = 7
    TracingStop = 8
    Zombie = 9
    Dead = 10
    WakeKill = 11
    Waking = 12
    Idle = 13
    Locked = 14
    Waiting = 15
    Suspended = 16
    Parked = 17

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
            return cls.Waking
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
