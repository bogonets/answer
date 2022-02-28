// Process Status
export const DAEMON_STATUS_RUNNING = 'running';
export const DAEMON_STATUS_SLEEPING = 'sleeping';
export const DAEMON_STATUS_DISK_SLEEP = 'disk-sleep';
export const DAEMON_STATUS_STOPPED = 'stopped';
export const DAEMON_STATUS_TRACING_STOP = 'tracing-stop';
export const DAEMON_STATUS_ZOMBIE = 'zombie';
export const DAEMON_STATUS_DEAD = 'dead';
export const DAEMON_STATUS_WAKE_KILL = 'wake-kill';
export const DAEMON_STATUS_WAKING = 'waking';
export const DAEMON_STATUS_IDLE = 'idle';  // Linux, macOS, FreeBSD
export const DAEMON_STATUS_LOCKED = 'locked';  // FreeBSD
export const DAEMON_STATUS_WAITING = 'waiting';  // FreeBSD
export const DAEMON_STATUS_SUSPENDED = 'suspended';  // NetBSD
export const DAEMON_STATUS_PARKED = 'parked';  // Linux
// Process Status Exception
export const DAEMON_STATUS_UNREGISTERED = 'unregistered';
export const DAEMON_STATUS_UNALLOCATED = 'unallocated';
export const DAEMON_STATUS_ERROR = 'error';

export function getStatusColor(status?: string) {
    if (typeof status === 'undefined') {
        return '';
    }
    switch (status) {
        case DAEMON_STATUS_RUNNING:
            return 'green';
        case DAEMON_STATUS_SLEEPING:
        case DAEMON_STATUS_DISK_SLEEP:
        case DAEMON_STATUS_STOPPED:
        case DAEMON_STATUS_TRACING_STOP:
            return 'blue';
        case DAEMON_STATUS_ZOMBIE:
            return 'deep-orange';
        case DAEMON_STATUS_DEAD:
        case DAEMON_STATUS_WAKE_KILL:
        case DAEMON_STATUS_WAKING:
        case DAEMON_STATUS_IDLE:
        case DAEMON_STATUS_LOCKED:
        case DAEMON_STATUS_WAITING:
        case DAEMON_STATUS_SUSPENDED:
        case DAEMON_STATUS_PARKED:
            return 'grey';
        case DAEMON_STATUS_UNREGISTERED:
        case DAEMON_STATUS_UNALLOCATED:
        case DAEMON_STATUS_ERROR:
            return 'red';
        default:
            return '';
    }
}

export function isStatusRunning(status: string) {
    switch (status) {
        case DAEMON_STATUS_RUNNING:
        case DAEMON_STATUS_SLEEPING:
        case DAEMON_STATUS_DISK_SLEEP:
        case DAEMON_STATUS_STOPPED:
        case DAEMON_STATUS_TRACING_STOP:
        case DAEMON_STATUS_ZOMBIE:
        case DAEMON_STATUS_DEAD:
        case DAEMON_STATUS_WAKE_KILL:
        case DAEMON_STATUS_WAKING:
        case DAEMON_STATUS_IDLE:
        case DAEMON_STATUS_LOCKED:
        case DAEMON_STATUS_WAITING:
        case DAEMON_STATUS_SUSPENDED:
        case DAEMON_STATUS_PARKED:
            return true;
        case DAEMON_STATUS_UNREGISTERED:
        case DAEMON_STATUS_UNALLOCATED:
        case DAEMON_STATUS_ERROR:
            return false;
        default:
            return false;
    }
}

export interface DaemonA {
    plugin: string;
    slug: string;
    name?: string;
    address?: string;
    requirements_sha256?: string;
    description?: string;
    extra?: any;
    enable: boolean;
    created_at?: string;
    updated_at?: string;

    status?: string;
    exit_code?: number;
}

export interface CreateDaemonQ {
    plugin: string;
    slug: string;
    name?: string;
    address?: string;
    description?: string;
    extra?: any;
    enable: boolean;
}

export interface UpdateDaemonQ {
    slug?: string;
    name?: string;
    address?: string;
    description?: string;
    extra?: any;
    enable?: boolean;
}
