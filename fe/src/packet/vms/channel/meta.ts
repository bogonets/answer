import type {VmsChannelEvent} from '@/packet/vms/channel/event';

export const VMS_CHANNEL_META_CODE_SUCCESS = 0;
export const VMS_CHANNEL_META_CODE_OPENED = 1;
export const VMS_CHANNEL_META_CODE_FILTERED = 2;
export const VMS_CHANNEL_META_CODE_BAD_ARGUMENT = -1;
export const VMS_CHANNEL_META_CODE_NOT_READY_ROI = -2;

export enum VmsChannelMetaCode {
  Success = 0,
  ChannelOpened = 1,
  Unknown = -1,
}

export interface VmsChannelMeta {
  code: VmsChannelMetaCode;
  events: Array<VmsChannelEvent>;
}
