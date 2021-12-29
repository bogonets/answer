export const ROLE_SLUG_OWNER = 'owner';

export interface RoleA {
    slug: string;
    name?: string;
    description?: string;
    extra?: any;
    hidden?: boolean;
    lock?: boolean;
    created_at?: string;
    updated_at?: string;
    permissions?: Array<string>;
}

export interface CreateRoleQ {
    slug: string;
    name?: string;
    description?: string;
    extra?: any;
    hidden?: boolean;
    lock?: boolean;
    permissions?: Array<string>;
}

export interface UpdateRoleQ {
    slug?: string;
    name?: string;
    description?: string;
    extra?: any;
    hidden?: boolean;
    lock?: boolean;
    permissions?: Array<string>;
}
