import type {VmsImageA} from '@/packet/vms/image';

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

export type VmsOnvifMediaSnapshotA = VmsImageA;
