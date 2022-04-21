export const VMS_CHANNEL_META_CONSUME_CODE_SUCCESS = 0;
export const VMS_CHANNEL_META_CONSUME_CODE_SKIP = 1;
export const VMS_CHANNEL_META_CONSUME_CODE_UNKNOWN = -1;

export enum VmsChannelMetaConsumeCode {
  Success = 0,
  Skip = 1,
  Unknown = -1,
}

export interface VmsChannelMetaConsume {
  code: VmsChannelMetaConsumeCode;
}
