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

export const VMS_SERVER_STATUS_UNKNOWN = 0;
export const VMS_SERVER_STATUS_NORMAL = 1;

export const DEFAULT_SERVER_ADDRESS = 'http://0.0.0.0:9999';

export const TRANSCEIVER_KIND_VIDEO = 'video';
export const TRANSCEIVER_KIND_AUDIO = 'audio';
export const DATA_CHANNEL_LABEL = 'meta';

export const DEFAULT_EVENT_UPDATE_INTERVAL_MILLISECONDS = SECOND_IN_MILLISECONDS;

const DEFAULT_STUN_SERVER_01 = 'stun:stun.l.google.com:19302';

const DEFAULT_ICE_SERVERS = [
    { urls: [DEFAULT_STUN_SERVER_01] }
] as Array<RTCIceServer>;

export const DEFAULT_RTC_CONFIGURATION = {
    sdpSemantics: 'unified-plan',
    // iceServers: [
    //     {
    //         urls: 'stun:192.168.0.6:3478',
    //     } as RTCIceServer,
    // ],
} as RTCConfiguration;

export const DEFAULT_VIDEO_TRANSCEIVER_INIT = {
    direction: 'recvonly'
} as RTCRtpTransceiverInit;

export const DEFAULT_AUDIO_TRANSCEIVER_INIT = {
    direction: 'recvonly'
} as RTCRtpTransceiverInit;

export const DEFAULT_DATA_CHANNEL_INIT = {
} as RTCDataChannelInit;

export const EVENT_CATEGORY_ID_COLOR = 1;
export const EVENT_CATEGORY_ID_DETECTION = 2;
export const EVENT_CATEGORY_ID_MATCHING = 3;
export const EVENT_CATEGORY_ID_OCR = 4;

export const EVENT_CATEGORY_NAME_COLOR = 'color';
export const EVENT_CATEGORY_NAME_DETECTION = 'detection';
export const EVENT_CATEGORY_NAME_MATCHING = 'matching';
export const EVENT_CATEGORY_NAME_OCR = 'ocr';
export const EVENT_CATEGORIES = [
    EVENT_CATEGORY_NAME_COLOR,
    EVENT_CATEGORY_NAME_DETECTION,
    EVENT_CATEGORY_NAME_MATCHING,
    EVENT_CATEGORY_NAME_OCR,
];

export const USER_CONFIG_REFRESH_INTERVAL = 1;
export const USER_CONFIG_POPUP = false;
export const USER_CONFIG_BEEP = false;
export const USER_CONFIG_BEEP_INTERVAL = 2;
export const USER_CONFIG_BEEP_DURATION = 10;

export const EVENT_CONFIG_OPERATOR_DEFAULT = '>=';
export const EVENT_CONFIG_OPERATORS = [
    '=',
    '!=',
    '>',
    '<',
    '>=',
    '<=',
];

export interface VmsImageA {
    content_type: string;
    encoding: string;
    content: string;
}

export function imageDataUrlToVmsImageA(image: string) {
    const prefix = 'data:';
    if (!image.startsWith(prefix)) {
        throw Error('Unsupported DataUrl');
    }

    const separatorIndex = image.indexOf(";");
    const typeStart = prefix.length;
    const typeLength = separatorIndex - prefix.length;
    const resultContentType = image.substr(typeStart, typeLength);

    const encodingStart = separatorIndex + 1;
    const commaIndex = image.indexOf(",", encodingStart);
    const encodingLength = commaIndex - encodingStart;
    const resultEncoding = image.substr(encodingStart, encodingLength);

    const contentBegin = commaIndex + 1;
    const resultContent = image.substr(contentBegin);

    return {
        content_type: resultContentType,
        encoding: resultEncoding,
        content: resultContent,
    } as VmsImageA;
}

export interface VmsUploadImageQ {
    content: string;
    name?: string;
    encoding?: string;
    content_type?: string;
}

export function imageDataUrlToVmsUploadImageQ(image: string, name?: string) {
    const vmsImageA = imageDataUrlToVmsImageA(image);
    return {
        content: vmsImageA.content,
        name: name,
        encoding: vmsImageA.encoding,
        content_type: vmsImageA.content_type,
    } as VmsUploadImageQ;
}

export interface VmsUploadImageA {
    name: string;
}

export interface VmsDeviceA {
    device_uid: number;
    group_slug: string;
    project_slug: string;
    name: string;
    description: string;
    stream_address: string;
    onvif_address: string;
    server_address: string;
    ai_address: string;
    ices: Array<string>;
    username: string;
    password: string;
    stream: string;
    protocol: string;
    active: boolean;
    daemon: boolean;
    created_at: string;
    updated_at: string;

    server_running?: boolean;
    server_status?: number;
    server_debugging?: boolean;
}

export interface VmsCreateDeviceQ {
    name: string;
    description: string;
    stream_address: string;
    onvif_address: string;
    server_address: string;
    ai_address: string;
    ices: Array<string>;
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
    stream_address?: string;
    ai_address?: string;
    onvif_address?: string;
    server_address?: string;
    ices?: Array<string>;
    username?: string;
    password?: string;
    stream?: string;
    protocol?: string;
    active?: boolean;
    daemon?: boolean;
}

export interface VmsLayoutA {
    layout_uid: number;
    group_slug: string;
    project_slug: string;
    name: string;
    description: string;
    index: number;
    device_uid: number;
    created_at: string;
    updated_at: string;
}

export interface VmsCreateLayoutQ {
    name: string;
    description: string;
    index: number;
    device_uid: number;
}

export interface VmsUpdateLayoutQ {
    group_slug?: string;
    project_slug?: string;
    name?: string;
    description?: string;
    index?: number;
    device_uid?: number;
}

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

export interface VmsEventTagA {
    event_uid: number;
    description: string;
    created_at: string;
    updated_at: string;
}

export interface VmsCreateEventTagQ {
    event_uid: number;
    description: string;
}

export interface VmsUpdateEventTagQ {
    description?: string;
}

export interface VmsEventA {
    event_uid: number;
    time: string;
    device_uid: number;
    category_id: number;
    event_config_uid: number;
    file: string;
    extra?: any;

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

export interface VmsEventImageA {
    content_type: string;
    encoding: string;
    content: string;
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

export interface VmsOnvifMediaSnapshotQ {
    snapshot_uri: string;
}

export interface VmsOnvifMediaSnapshotA {
    content_type: string;
    encoding: string;
    content: string;
}

export interface IceServerA {
    urls: string;
    username?: string;
    credential?: string;
    credential_type?: string;
}

export interface RtcOfferQ {
    type: string;
    sdp: string;
}

export interface RtcAnswerA {
    peer_id: number;
    type: string;
    sdp: string;
}

export interface VmsEventConfigColorQ {
    red: number;
    green: number;
    blue: number;
    threshold: number;
    operator: string;
    emit_condition: boolean;
    x1: number;
    y1: number;
    x2: number;
    y2: number;
}

export interface VmsEventConfigDetectionQ {
    model: string;
    checkpoint: string;
    label: Array<string>;
    threshold: number;
    x1: number;
    y1: number;
    x2: number;
    y2: number;
}

export interface VmsEventConfigMatchingQ {
    train_image_uuid: string;
    train_x1: number;
    train_y1: number;
    train_x2: number;
    train_y2: number;
    distance: number;
    threshold: number;
    operator: string;
    emit_condition: boolean;
    x1: number;
    y1: number;
    x2: number;
    y2: number;
}

export interface VmsEventConfigOcrFilterQ {
    logical: string;
    operator: string;
    value: number;
}

export interface VmsEventConfigOcrQ {
    model: string;
    checkpoint: string;
    threshold: number;
    filters: Array<VmsEventConfigOcrFilterQ>
    x1: number;
    y1: number;
    x2: number;
    y2: number;
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

export const VMS_CHANNEL_META_CODE_SUCCESS = 0;
export const VMS_CHANNEL_META_CODE_OPENED = 1;
export const VMS_CHANNEL_META_CODE_FILTERED = 2;
export const VMS_CHANNEL_META_CODE_BAD_ARGUMENT = -1;
export const VMS_CHANNEL_META_CODE_NOT_READY_ROI = -2;

export interface VmsChannelMeta {
    code: number;
    message: string;

    content?: any;

    x1?: number;
    y1?: number;
    x2?: number;
    y2?: number;
    score?: number;
}

export const VMS_CHANNEL_META_CONSUME_CODE_SUCCESS = 0;
export const VMS_CHANNEL_META_CONSUME_CODE_SKIP = 1;
export const VMS_CHANNEL_META_CONSUME_CODE_UNKNOWN_ERRORS = -1;

export interface VmsChannelMetaConsume {
    code: number;
}

export function createEmptyVmsDeviceA() {
    return {
        device_uid: 0,
        group_slug: '',
        project_slug: '',
        name: '',
        description: '',
        stream_address: '',
        onvif_address: '',
        server_address: '',
        ai_address: '',
        ices: [],
        username: '',
        password: '',
        stream: '',
        protocol: '',
        active: false,
        daemon: false,
        created_at: '',
        updated_at: '',
    } as VmsDeviceA;
}
