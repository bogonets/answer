export interface DaemonA {
    plugin: string;
    name: string;
    address?: string;
    requirements_sha256?: string;
    description?: string;
    extra?: any;
    enable: boolean;
    created_at?: string;
    updated_at?: string;

    running?: boolean;
    exit_code?: number;
}

export interface CreateDaemonQ {
    plugin: string;
    name: string;
    address?: string;
    description?: string;
    extra?: any;
    enable: boolean;
}

export interface UpdateDaemonQ {
    name: string;
    address?: string;
    description?: string;
    extra?: any;
    enable?: boolean;
}
