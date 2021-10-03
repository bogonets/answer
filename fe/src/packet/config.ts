export interface ConfigA {
    key: string;
    type: string;
    value: string;
}

export interface UpdateConfigValueQ {
    value: string;
}

export function createEmptyConfigA() {
    return {
        key: '',
        type: '',
        value: '',
    } as ConfigA;
}
