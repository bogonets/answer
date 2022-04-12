export enum DaemonState {
  Unknown = 0,
  Unregistered = 1,
  EnvNotFound = 2,
  EnvCreating = 3,
  Down = 4,
  Running = 5,
  Sleeping = 6,
  DiskSleep = 7,
  Stopped = 8,
  TracingStop = 9,
  Zombie = 10,
  Dead = 11,
  WakeKill = 12,
  Waking = 13,
  Idle = 14,
  Locked = 15,
  Waiting = 16,
  Suspended = 17,
  Parked = 18,
}

export function getStateName(state: DaemonState) {
  switch (state) {
    case DaemonState.Unknown:
      return 'Unknown';
    case DaemonState.Unregistered:
      return 'Unregistered';
    case DaemonState.EnvNotFound:
      return 'EnvNotFound';
    case DaemonState.EnvCreating:
      return 'EnvCreating';
    case DaemonState.Down:
      return 'Down';
    case DaemonState.Running:
      return 'Running';
    case DaemonState.Sleeping:
      return 'Sleeping';
    case DaemonState.DiskSleep:
      return 'DiskSleep';
    case DaemonState.Stopped:
      return 'Stopped';
    case DaemonState.TracingStop:
      return 'TracingStop';
    case DaemonState.Zombie:
      return 'Zombie';
    case DaemonState.Dead:
      return 'Dead';
    case DaemonState.WakeKill:
      return 'WakeKill';
    case DaemonState.Waking:
      return 'Waking';
    case DaemonState.Idle:
      return 'Idle';
    case DaemonState.Locked:
      return 'Locked';
    case DaemonState.Waiting:
      return 'Waiting';
    case DaemonState.Suspended:
      return 'Suspended';
    case DaemonState.Parked:
      return 'Parked';
    default:
      return `UnknownState(${state})`;
  }
}

export function getStateColor(state: DaemonState) {
  switch (state) {
    case DaemonState.Unknown:
      return 'red';
    case DaemonState.Unregistered:
    case DaemonState.EnvNotFound:
    case DaemonState.EnvCreating:
    case DaemonState.Down:
      return 'grey';
    case DaemonState.Running:
      return 'green';
    case DaemonState.Sleeping:
    case DaemonState.DiskSleep:
    case DaemonState.Stopped:
    case DaemonState.TracingStop:
      return 'blue';
    case DaemonState.Zombie:
      return 'deep-orange';
    case DaemonState.Dead:
    case DaemonState.WakeKill:
    case DaemonState.Waking:
    case DaemonState.Idle:
    case DaemonState.Locked:
    case DaemonState.Waiting:
    case DaemonState.Suspended:
    case DaemonState.Parked:
      return 'grey';
    default:
      return 'red';
  }
}

export function isStateRunning(state: DaemonState) {
  switch (state) {
    case DaemonState.Unknown:
    case DaemonState.Unregistered:
    case DaemonState.EnvNotFound:
    case DaemonState.EnvCreating:
    case DaemonState.Down:
      return false;
    case DaemonState.Running:
    case DaemonState.Sleeping:
    case DaemonState.DiskSleep:
    case DaemonState.Stopped:
    case DaemonState.TracingStop:
      return true;
    case DaemonState.Zombie:
      return false;
    case DaemonState.Dead:
      return false;
    case DaemonState.WakeKill:
    case DaemonState.Waking:
    case DaemonState.Idle:
    case DaemonState.Locked:
    case DaemonState.Waiting:
    case DaemonState.Suspended:
    case DaemonState.Parked:
      return true;
    default:
      return false;
  }
}

export interface DaemonA {
  plugin: string;
  slug: string;
  name: string;
  address: string;
  description: string;
  enable: boolean;
  created_at: string;
  updated_at: string;

  state: DaemonState;
  exit_code?: number;
}

export interface CreateDaemonQ {
  plugin: string;
  slug: string;
  name?: string;
  address?: string;
  description?: string;
  enable: boolean;
}

export interface UpdateDaemonQ {
  slug?: string;
  name?: string;
  address?: string;
  description?: string;
  enable?: boolean;
}
