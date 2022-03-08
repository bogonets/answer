# -*- coding: utf-8 -*-

from enum import Enum


class DaemonState(Enum):
    Unknown = 0
    Unregistered = 1
    EnvNotFound = 2
    EnvCreating = 3
    Down = 4

    Running = 5
    Sleeping = 6
    DiskSleep = 7
    Stopped = 8
    TracingStop = 9
    Zombie = 10
    Dead = 11
    WakeKill = 12
    Waking = 13
    Idle = 14
    Locked = 15
    Waiting = 16
    Suspended = 17
    Parked = 18

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
