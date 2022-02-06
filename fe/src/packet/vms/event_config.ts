import {VmsEventConfigColorQ} from '@/packet/vms/extra/color_matching';
import {VmsEventConfigMatchingQ} from '@/packet/vms/extra/feature_matching';
import {VmsEventConfigDetectionQ} from '@/packet/vms/extra/object_detector';
import {VmsEventConfigOcrQ} from '@/packet/vms/extra/seven_segment_detector';

export const EVENT_CONFIG_OPERATOR_DEFAULT = '>=';
export const EVENT_CONFIG_OPERATORS = [
    '=',
    '!=',
    '>',
    '<',
    '>=',
    '<=',
];

export type VmsEventConfigExtra = VmsEventConfigColorQ
    | VmsEventConfigMatchingQ
    | VmsEventConfigDetectionQ
    | VmsEventConfigOcrQ;

export interface VmsEventConfigA {
    event_config_uid: number;
    sequence: number;
    device_uid: number;
    category: string;
    name: string;
    enable: boolean;
    extra?: VmsEventConfigExtra;
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
