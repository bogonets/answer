import type {PreferenceA} from '@/packet/preference';
import {newPreference} from '@/packet/preference';

export interface UserExtraA {
  dark?: boolean;
  lang?: string;
  timezone?: string;
}

export interface VmsUserExtraA extends UserExtraA {
  vmsRefreshInterval?: number;
  vmsPopup?: boolean;
  vmsBeep?: boolean;
  vmsBeepInterval?: number;
  vmsBeepDuration?: number;
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
  password: string; // Perhaps the client encoded it with `SHA256 HEX string`.
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

export function newUserA(
  username?: string,
  nickname?: string,
  email?: string,
  phone1?: string,
  phone2?: string,
  is_admin?: boolean,
  extra?: any, // eslint-disable-line @typescript-eslint/no-explicit-any
  created_at?: string,
  updated_at?: string,
  last_login?: string,
) {
  return {
    username: username ?? '',
    nickname: nickname ?? '',
    email: email ?? '',
    phone1: phone1 ?? '',
    phone2: phone2 ?? '',
    is_admin: !!is_admin,
    extra: extra ?? newUserExtraA(),
    created_at: created_at ?? '',
    updated_at: updated_at ?? '',
    last_login: last_login ?? '',
  } as UserA;
}

export function newSigninA(access?: string, refresh?: string) {
  return {
    access: access ?? '',
    refresh: refresh ?? '',
    user: newUserA(),
    preference: newPreference(),
  } as SigninA;
}

export function newSignupQ(
  username?: string,
  password?: string,
  nickname?: string,
  email?: string,
  phone1?: string,
  phone2?: string,
  is_admin?: boolean,
  extra?: any, // eslint-disable-line @typescript-eslint/no-explicit-any
) {
  return {
    username: username ?? '',
    password: password ?? '',
    nickname: nickname ?? '',
    email: email ?? '',
    phone1: phone1 ?? '',
    phone2: phone2 ?? '',
    is_admin: !!is_admin,
    extra: extra ?? newUserExtraA(),
  } as SignupQ;
}

export function newUserExtraA(dark?: boolean, lang?: string, timezone?: string) {
  return {
    dark: !!dark,
    lang: lang ?? '',
    timezone: timezone ?? '',
  } as UserExtraA;
}
