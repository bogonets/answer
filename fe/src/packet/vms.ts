export const STREAM_TYPE_RTP_UNICAST = 'RTP-Unicast';
export const STREAM_TYPE_RTP_MULTICAST = 'RTP-Multicast';
export const STREAM_TYPES = [
    STREAM_TYPE_RTP_UNICAST,
    STREAM_TYPE_RTP_MULTICAST,
];


export const PROTOCOL_UDP = 'UDP';
export const PROTOCOL_TCP = 'TCP';
export const PROTOCOL_RTSP = 'RTSP';
export const PROTOCOL_HTTP = 'HTTP';
export const PROTOCOLS = [
    PROTOCOL_UDP,
    PROTOCOL_TCP,
    PROTOCOL_RTSP,
    PROTOCOL_HTTP,
];

export interface VmsDeviceA {
    device_uid: number;
    group_slug: string;
    project_slug: string;
    name: string;
    description: string;
    url: string;
    onvif_url: string;
    username: string;
    password: string;
    stream: string;
    protocol: string;
    active: boolean;
    daemon: boolean;
    created_at: string;
    updated_at: string;
}

export interface CreateVmsDeviceQ {
    name: string;
    description: string;
    url: string;
    onvif_url: string;
    username: string;
    password: string;
    stream: string;
    protocol: string;
    active: boolean;
    daemon: boolean;
}

export interface UpdateVmsDeviceQ {
    group_slug?: string;
    project_slug?: string;
    name?: string;
    description?: string;
    url?: string;
    onvif_url?: string;
    username?: string;
    password?: string;
    stream?: string;
    protocol?: string;
    active?: boolean;
    daemon?: boolean;
}

export interface VmsDeviceDiscoveryQ {
    session: string;
    username: string;
    password: string;
    timeout: number;
}

export interface VmsDeviceDiscoveryA {
    expired: string;
}

export interface VmsDeviceDiscoveryInterpolationQ {
    session: string;
}

export interface VmsDeviceDiscoveryInterpolationA {
    type: string;
    device: string;
    ip: string;
    profile: string;
    url: string;
}
