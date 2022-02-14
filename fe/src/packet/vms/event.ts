import type {VmsImageA} from '@/packet/vms/image';
import type {VmsChannelEvent} from '@/packet/vms/channel/event';

export interface VmsEventA {
    event_uid: number;
    time: string;
    device_uid: number;
    category_id: number;
    event_config_uid: number;
    directory: string;
    filename: string;
    extra?: VmsChannelEvent;

    description?: null | string;
}

export interface VmsFilterEventQ {
    date: string;
    device_uid?: number;
    category?: string;
}

export interface VmsNewsEventQ {
    time: string;
    max: number;
}

export interface VmsLatestEventQ {
    max: number;
}

export type VmsEventImageA = VmsImageA;
