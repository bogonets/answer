export interface PortA {
    number: number;
    sock: number;
    ref_uid?: number;
    ref_category?: string;
    created_at: string;
    updated_at: string;
}

export interface PortRangeA {
    min: number;
    max: number;
}
