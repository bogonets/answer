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
