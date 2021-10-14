export interface VmsDeviceA {
    type: string;
    device: string;
    name: string;
    url: string;
    user: string;
    online: boolean;
}

export interface VmsCreateDeviceQ {
    url: string;
    username: string;
    password: string;
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
