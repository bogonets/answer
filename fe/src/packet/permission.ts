export interface RawPermission {
    r_layout: boolean;
    w_layout: boolean;
    r_storage: boolean;
    w_storage: boolean;
    r_manager: boolean;
    w_manager: boolean;
    r_graph: boolean;
    w_graph: boolean;
    r_member: boolean;
    w_member: boolean;
    r_setting: boolean;
    w_setting: boolean;
    is_admin: boolean;
    features: Array<string>;
    extra: any;
}

export interface PermissionA {
    slug: string;
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
    hidden?: boolean;
    lock?: boolean;
    created_at?: string;
    updated_at?: string;
}

export interface CreatePermissionQ {
    slug: string;
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
    hidden?: boolean;
    lock?: boolean;
}

export interface UpdatePermissionQ {
    slug?: string;
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
    hidden?: boolean;
    lock?: boolean;
}

export const PERMISSION_SLUG_GUEST = 'guest';
export const PERMISSION_SLUG_REPORTER = 'reporter';
export const PERMISSION_SLUG_OPERATOR = 'operator';
export const PERMISSION_SLUG_MAINTAINER = 'maintainer';
export const PERMISSION_SLUG_OWNER = 'owner';
