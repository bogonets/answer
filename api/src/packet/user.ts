import type {PreferenceA} from './preference';
import {newPreference} from './preference';

export interface UserA {
  username: string;
  nickname: string;
  email: string;
  phone: string;
  admin: boolean;
  dark: number;
  lang: string;
  timezone: string;
  created_at: string;
  updated_at: string;
  last_login?: string;
}

export interface UserInfoA {
  key: string;
  value: string;
  created_at: string;
  updated_at: string;
}

export interface UpdateUserQ {
  nickname?: string;
  email?: string;
  phone?: string;
  admin?: boolean;
  dark?: number;
  lang?: string;
  timezone?: string;
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
  phone?: string;
  admin?: boolean;
  dark?: number;
  lang?: string;
  timezone?: string;
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
  phone?: string,
  admin?: boolean,
  dark?: number,
  lang?: string,
  timezone?: string,
  created_at?: string,
  updated_at?: string,
  last_login?: string,
) {
  return {
    username: username ?? '',
    nickname: nickname ?? '',
    email: email,
    phone: phone,
    admin: !!admin,
    dark: dark ?? 0,
    lang: lang ?? '',
    timezone: timezone ?? '',
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
  phone?: string,
  admin?: boolean,
  dark?: number,
  lang?: string,
  timezone?: string,
) {
  return {
    username: username ?? '',
    password: password ?? '',
    nickname: nickname ?? '',
    email: email,
    phone: phone,
    admin: !!admin,
    dark: dark ?? 0,
    lang: lang ?? '',
    timezone: timezone ?? '',
  } as SignupQ;
}
