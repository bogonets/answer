export interface VmsDeviceA {
    type: string;
    device: string;
    name: string;
    url: string;
    user: string;
    online: boolean;
}

export interface VmsDeviceDiscoveryQ {
    session: string;
    user: string;
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
