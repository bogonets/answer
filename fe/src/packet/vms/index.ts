export * from '@/packet/vms/channel/event';
export * from '@/packet/vms/channel/meta';
export * from '@/packet/vms/channel/meta_consume';
export * from '@/packet/vms/extra/color_matching';
export * from '@/packet/vms/extra/feature_matching';
export * from '@/packet/vms/extra/object_detector';
export * from '@/packet/vms/extra/seven_segment_detector';
export * from '@/packet/vms/device';
export * from '@/packet/vms/discovery';
export * from '@/packet/vms/event';
export * from '@/packet/vms/event_category';
export * from '@/packet/vms/event_config';
export * from '@/packet/vms/event_tag';
export * from '@/packet/vms/image';
export * from '@/packet/vms/layout';
export * from '@/packet/vms/onvif';
export * from '@/packet/vms/rtc';

export const STREAM_TYPE_RTP_UNICAST = 'RTP-Unicast';
export const STREAM_TYPE_RTP_MULTICAST = 'RTP-Multicast';
export const STREAM_TYPES = [STREAM_TYPE_RTP_UNICAST, STREAM_TYPE_RTP_MULTICAST];

export const PROTOCOL_UDP = 'UDP';
export const PROTOCOL_TCP = 'TCP';
export const PROTOCOL_RTSP = 'RTSP';
export const PROTOCOL_HTTP = 'HTTP';
export const PROTOCOLS = [PROTOCOL_UDP, PROTOCOL_TCP, PROTOCOL_RTSP, PROTOCOL_HTTP];

export const SECOND_IN_MILLISECONDS = 1000;
export const MINUTE_IN_MILLISECONDS = 60 * SECOND_IN_MILLISECONDS;

export const DISCOVERY_HEARTBEAT_INTERVAL = SECOND_IN_MILLISECONDS;
export const DISCOVERY_LEEWAY_SECONDS = 1;

export const MEDIA_SERVER_STATUS_CREATE = 0;
export const MEDIA_SERVER_STATUS_BEGINNING = 1;
export const MEDIA_SERVER_STATUS_RUNNING = 2;
export const MEDIA_SERVER_STATUS_ENDING = 3;
export const MEDIA_SERVER_STATUS_RESTARTING = 4;
export const MEDIA_SERVER_STATUS_PAUSED = 5;
export const MEDIA_SERVER_STATUS_EXITED = 6;
export const MEDIA_SERVER_STATUS_DEAD = 7;

export const USER_CONFIG_REFRESH_INTERVAL = 1;
export const USER_CONFIG_POPUP = false;
export const USER_CONFIG_BEEP = false;
export const USER_CONFIG_BEEP_INTERVAL = 2;
export const USER_CONFIG_BEEP_DURATION = 10;

export const DEFAULT_SERVER_ADDRESS = 'http://0.0.0.0:9999';
export const DEFAULT_EVENT_UPDATE_INTERVAL_MILLISECONDS = SECOND_IN_MILLISECONDS;
