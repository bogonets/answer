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

export const SECOND_IN_MILLISECONDS = 1000;
export const MINUTE_IN_MILLISECONDS = 60 * SECOND_IN_MILLISECONDS;

export const DISCOVERY_HEARTBEAT_INTERVAL = SECOND_IN_MILLISECONDS;
export const DISCOVERY_LEEWAY_SECONDS = 1;

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

export interface VmsCreateDeviceQ {
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

export interface VmsUpdateDeviceQ {
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

export interface VmsDiscoveryQ {
    timeout: number;
    session: string;
    ipv6: boolean;
}

export interface VmsDiscoveredDeviceA {
    epr: string;
    address: string;
    types: Array<string>;
    scopes: Array<string>;
}

export interface VmsDiscoveredHeartbeatQ {
    session: string;
}

export interface VmsDiscoveredHeartbeatA {
    done: boolean;
    devices?: Array<VmsDiscoveredDeviceA>;
}

export interface VmsOnvifMediaStreamUriQ {
    address: string;
    username: string;
    password: string;
    timeout: number;
    session: string;
    digest: boolean;
    protocol: string;
    stream: string;
}

export interface VmsOnvifMediaStreamUriA {
    profile_name: string;
    profile_token: string;
    stream_uri: string;
    snapshot_uri: string;
}

export interface VmsOnvifMediaStreamUriHeartbeatQ {
    session: string;
}

export interface VmsOnvifMediaStreamUriHeartbeatA {
    done: boolean;
    medias?: Array<VmsOnvifMediaStreamUriA>;
}


// export interface VmsDeviceDiscoveryA {
//     expired: string;
// }
//
// export interface VmsDeviceDiscoveryInterpolationQ {
//     session: string;
// }
//
// export interface VmsDeviceDiscoveryInterpolationA {
//     type: string;
//     device: string;
//     ip: string;
//     profile: string;
//     url: string;
// }
