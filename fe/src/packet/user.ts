import {PreferenceA, createEmptyPreference} from '@/packet/preference';

export interface UserExtraA {
    dark?: boolean;
    lang?: string;
    timezone?: string;
}

export interface UserA {
    username: string;
    nickname?: string;
    email?: string;
    phone1?: string;
    phone2?: string;
    is_admin?: boolean;
    extra?: UserExtraA;
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
    extra?: UserExtraA;
}

export interface SigninA {
    access: string;
    refresh: string;
    user: UserA;
    preference: PreferenceA;
}

export interface SignupQ {
    username: string;
    password: string;  // Perhaps the client encoded it with SHA256.
    nickname?: string;
    email?: string;
    phone1?: string;
    phone2?: string;
    is_admin?: boolean;
    extra?: UserExtraA;
}

export interface UpdatePasswordQ {
    before: string;
    after: string;
}

export interface RefreshTokenA {
    access: string;
}

export function createEmptyUserA() {
    return {
        username: '',
        nickname: '',
        email: '',
        phone1: '',
        phone2: '',
        is_admin: false,
        extra: createEmptyUserExtraA(),
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
        preference: createEmptyPreference(),
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
        extra: createEmptyUserExtraA(),
    } as SignupQ;
}

export function createEmptyUserExtraA() {
    return {
        dark: false,
        lang: '',
        timezone: '',
    } as UserExtraA;
}
