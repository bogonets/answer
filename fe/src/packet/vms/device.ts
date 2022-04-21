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

export interface IceServerA {
  urls: string;
  username?: string;
  credential?: string;
  credential_type?: string;
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
