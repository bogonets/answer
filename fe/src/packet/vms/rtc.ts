export const TRANSCEIVER_KIND_VIDEO = 'video';
export const TRANSCEIVER_KIND_AUDIO = 'audio';
export const DATA_CHANNEL_LABEL = 'meta';

export const DEFAULT_STUN_SERVER_01 = 'stun:stun.l.google.com:19302';

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

// -------
// Packets
// -------

export interface RtcOfferQ {
    type: string;
    sdp: string;
}

export interface RtcAnswerA {
    peer_id: number;
    type: string;
    sdp: string;
}
