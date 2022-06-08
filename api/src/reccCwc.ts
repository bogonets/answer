import type {ReccApiOptions} from './reccApiBase';

export const MESSAGE_EVENT_TYPE = 'message';

export const MESSAGE_DATA_TYPE_INIT = 'recc/init';
export const MESSAGE_DATA_TYPE_TOAST = 'recc/toast';
export const MESSAGE_DATA_TYPE_MOVE = 'recc/move';
export const MESSAGE_DATA_TYPE_FULLSCREEN = 'recc/fullscreen';
export const MESSAGE_DATA_TYPE_REFRESH_TOKEN_ERROR = 'recc/refreshTokenError';
export const MESSAGE_DATA_TYPE_RENEWAL_ACCESS_TOKEN = 'recc/renewalAccessToken';
export const MESSAGE_DATA_TYPE_UNINITIALIZED_SERVICE = 'recc/uninitializedService';

export interface ReccCwcDataInit {
  apiOptions: ReccApiOptions;
  dark: boolean;
  lang: string;

  group?: string;
  project?: string;
}

export enum ToastLevel {
  Success,
  Info,
  Warning,
  Error,
  RequestSuccess,
  RequestFailure,
}

export interface ReccCwcDataToast {
  level: ToastLevel;
  message?: string;
  detail?: string;
}

export interface ReccCwcDataMove {
  name?: string;
  path?: string;
  params?: object;
}

export interface ReccCwcDataFullscreen {
  fullscreen?: boolean;
  flip?: boolean;
}

export interface ReccCwcDataRenewalAccessToken {
  accessToken: string;
}

export type ReccCwcDataAny =
  | ReccCwcDataInit
  | ReccCwcDataToast
  | ReccCwcDataMove
  | ReccCwcDataFullscreen
  | ReccCwcDataRenewalAccessToken;

export interface ReccCwcMessage {
  type: string;
  data?: ReccCwcDataAny;
}

export function postMessage(w: Window, m: ReccCwcMessage) {
  w.postMessage(m, w.origin);
}

export function postInit(w: Window, data: ReccCwcDataInit) {
  postMessage(w, {type: MESSAGE_DATA_TYPE_INIT, data});
}

export function postToast(w: Window, data: ReccCwcDataToast) {
  postMessage(w, {type: MESSAGE_DATA_TYPE_TOAST, data});
}

export function postMove(w: Window, data: ReccCwcDataMove) {
  postMessage(w, {type: MESSAGE_DATA_TYPE_MOVE, data});
}

export function postFullscreen(w: Window, data: ReccCwcDataFullscreen) {
  postMessage(w, {type: MESSAGE_DATA_TYPE_FULLSCREEN, data});
}

export function postRefreshTokenError(w: Window) {
  postMessage(w, {type: MESSAGE_DATA_TYPE_REFRESH_TOKEN_ERROR});
}

export function postRenewalAccessToken(w: Window, data: ReccCwcDataRenewalAccessToken) {
  postMessage(w, {type: MESSAGE_DATA_TYPE_RENEWAL_ACCESS_TOKEN, data});
}

export function postUninitializedService(w: Window) {
  postMessage(w, {type: MESSAGE_DATA_TYPE_UNINITIALIZED_SERVICE});
}
