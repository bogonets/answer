export interface PermissionA {
    name: string;
    description?: string;
    features?: Array<string>;
    extra?: any;
    r_layout?: boolean;
    w_layout?: boolean;
    r_storage?: boolean;
    w_storage?: boolean;
    r_manager?: boolean;
    w_manager?: boolean;
    r_graph?: boolean;
    w_graph?: boolean;
    r_member?: boolean;
    w_member?: boolean;
    r_setting?: boolean;
    w_setting?: boolean;
    created_at?: string;
    updated_at?: string;
}

export interface CreatePermissionQ {
    name: string;
    description?: string;
    features?: Array<string>;
    extra?: any;
    r_layout?: boolean;
    w_layout?: boolean;
    r_storage?: boolean;
    w_storage?: boolean;
    r_manager?: boolean;
    w_manager?: boolean;
    r_graph?: boolean;
    w_graph?: boolean;
    r_member?: boolean;
    w_member?: boolean;
    r_setting?: boolean;
    w_setting?: boolean;
}

export interface UpdatePermissionQ {
    name?: string;
    description?: string;
    features?: Array<string>;
    extra?: any;
    r_layout?: boolean;
    w_layout?: boolean;
    r_storage?: boolean;
    w_storage?: boolean;
    r_manager?: boolean;
    w_manager?: boolean;
    r_graph?: boolean;
    w_graph?: boolean;
    r_member?: boolean;
    w_member?: boolean;
    r_setting?: boolean;
    w_setting?: boolean;
}
