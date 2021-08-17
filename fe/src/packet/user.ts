export interface UserA {
    username: string;
    nickname?: string;
    email?: string;
    phone1?: string;
    phone2?: string;
    is_admin?: boolean;
    extra?: any;
    created_at?: string;
    updated_at?: string;
    last_login?: string;
}

export interface UpdateUserQ {
    nickname?: string;
    email?: string;
    phone1?: string;
    phone2?: string;
    is_admin?: boolean;
    extra?: any;
}

export interface SigninA {
    access: string;
    refresh: string;
    user: UserA;
}

export interface SignupQ {
    username: string;
    password: string;  // Perhaps the client encoded it with SHA256.
    nickname?: string;
    email?: string;
    phone1?: string;
    phone2?: string;
    is_admin?: boolean;
    extra?: any;
}

export interface UpdatePasswordQ {
    before: string;
    after: string;
}

// -----------
// Client only
// -----------

export interface UserExtra {
    dark?: boolean;
    lang?: string;
}

export function createEmptyUserA() {
    return {
        username: '',
        nickname: '',
        email: '',
        phone1: '',
        phone2: '',
        is_admin: false,
        extra: createEmptyUserExtra(),
        created_at: '',
        updated_at: '',
        last_login: '',
    } as UserA;
}

export function createEmptySigninA() {
    return {
        access: '',
        refresh: '',
        user: createEmptyUserA(),
    } as SigninA;
}

export function createEmptySignupQ() {
    return {
        username: '',
        password: '',
        nickname: '',
        email: '',
        phone1: '',
        phone2: '',
        is_admin: false,
        extra: createEmptyUserExtra(),
    } as SignupQ;
}

export function createEmptyUserExtra() {
    return {
        dark: false,
        lang: '',
    } as UserExtra;
}