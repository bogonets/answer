export interface ContainerA {
    key: string;
    name: string;
    status: string;
    image: string;
    created: string;
    labels: object;
    ports: object;
}

export const STATUS_CREATED = 'Created';
export const STATUS_RESTARTING = 'Restarting';
export const STATUS_RUNNING = 'Running';
export const STATUS_REMOVING = 'Removing';
export const STATUS_PAUSED = 'Paused';
export const STATUS_EXITED = 'Exited';
export const STATUS_DEAD = 'Dead';

export interface ControlContainersQ {
    keys: Array<string>;
    operator: string;
    signal?: string;
    force?: boolean;
}

export const CONTROL_OPERATOR_START = 'Start';
export const CONTROL_OPERATOR_STOP = 'Stop';
export const CONTROL_OPERATOR_KILL = 'Kill';
export const CONTROL_OPERATOR_RESTART = 'Restart';
export const CONTROL_OPERATOR_PAUSE = 'Pause';
export const CONTROL_OPERATOR_RESUME = 'Resume';
export const CONTROL_OPERATOR_REMOVE = 'Remove';
