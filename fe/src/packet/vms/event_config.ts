export const EVENT_CONFIG_OPERATOR_DEFAULT = '>=';
export const EVENT_CONFIG_OPERATORS = [
    '=',
    '!=',
    '>',
    '<',
    '>=',
    '<=',
];

export interface VmsEventConfigA {
    event_config_uid: number;
    sequence: number;
    device_uid: number;
    category: string;
    name: string;
    enable: boolean;
    extra?: any;
    created_at: string;
    updated_at: string;
}

export interface VmsCreateEventConfigQ {
    sequence: number;
    device_uid: number;
    category: string;
    name: string;
    enable: boolean;
    extra?: any;
}

export interface VmsUpdateEventConfigQ {
    sequence?: number;
    device_uid?: number;
    category?: string;
    name?: string;
    enable?: boolean;
    extra?: any;
}
