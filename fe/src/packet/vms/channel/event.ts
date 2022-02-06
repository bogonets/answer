import {EventCategory} from '@/packet/vms/event_category';

export enum VmsChannelEventCode {
    // Normal
    Emit = 0,
    Skip = 1,
    Disabled = 2,

    // Errors
    NotReadyRoi = -1,
    NotReadyFilters = -2,
}

export interface VmsChannelEventItem {
    score?: number;
}

export interface VmsChannelEvent {
    code: VmsChannelEventCode;
    message: string;
    category: EventCategory;

    items: Array<VmsChannelEventItem>;
}
