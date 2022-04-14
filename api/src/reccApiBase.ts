import AxiosLib from 'axios';
import type {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosError,
  AxiosRequestHeaders,
} from 'axios';
import {sha256hex} from './crypto';
import type {RefreshTokenA} from './packet/user';
import {UninitializedServiceError, RefreshTokenError} from './error';

export const DEFAULT_TIMEOUT_MILLISECONDS = 30 * 1000;
export const STATUS_CODE_UNAUTHORIZED = 401;
export const STATUS_CODE_UNINITIALIZED_SERVICE = 561;
export const VALIDATE_STATUS = [200];
export const HEADER_AUTHORIZATION = 'Authorization';
export const HEADER_RECC_REFRESH_TOKEN = 'Recc-Refresh-Token';
export const PATH_TOKEN_REFRESH = '/public/token/refresh';
export const DEFAULT_API_VERSION = 2;
export const DEFAULT_ACCEPT = 'application/json';

export function originToBaseUrl(origin: string, version: number): string {
  if (origin[origin.length - 1] == '/') {
    return origin + `api/v${version}`;
  } else {
    return origin + `/api/v${version}`;
  }
}

export interface ReccApiOptions {
  origin?: string;
  timeout?: number;
  validateStatus?: Array<number>;
  accept?: string;
  logging?: boolean;
  version?: number;

  onRefreshTokenError?: () => void;
  onRenewalAccessToken?: (accessToken: string) => void;
  onUninitializedService?: () => void;
}

export class ReccApiBase {
  originAddress: string;
  validateStatus: Array<number>;
  apiVersion: number;
  logging: boolean;

  onRefreshTokenError?: () => void;
  onRenewalAccessToken?: (accessToken: string) => void;
  onUninitializedService?: () => void;
  onRegisterRefreshSubscribers?: (config: AxiosRequestConfig) => void;
  onUnregisterRefreshSubscribers?: (config: AxiosRequestConfig) => void;

  accessToken = '';
  refreshToken = '';
  axios: AxiosInstance;

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  refreshSubscribers = [] as Array<(access?: string) => any>;
  refreshing = false;

  constructor(options?: ReccApiOptions) {
    const origin = options?.origin || document.location.origin;
    const timeout = options?.timeout || DEFAULT_TIMEOUT_MILLISECONDS;
    const validate = options?.validateStatus || VALIDATE_STATUS;
    const accept = options?.accept || DEFAULT_ACCEPT;
    const version = options?.version || DEFAULT_API_VERSION;
    const logging = options?.logging || false;

    this.originAddress = origin;
    this.validateStatus = validate;
    this.apiVersion = version;
    this.logging = logging;
    this.onRefreshTokenError = options?.onRefreshTokenError;
    this.onRenewalAccessToken = options?.onRenewalAccessToken;
    this.onUninitializedService = options?.onUninitializedService;
    this.onRegisterRefreshSubscribers = undefined;
    this.onUnregisterRefreshSubscribers = undefined;

    this.axios = AxiosLib.create({
      baseURL: originToBaseUrl(origin, version),
      timeout: timeout,
      headers: {Accept: accept},
      validateStatus: (status: number): boolean => {
        return VALIDATE_STATUS.includes(status);
      },
    });
    this.axios.interceptors.response.use(
      response => response,
      error => this.onResponseRejected(error),
    );
  }

  get refreshConfig() {
    const headers = {} as AxiosRequestHeaders;
    headers[HEADER_AUTHORIZATION] = `Bearer ${this.refreshToken}`;
    headers[HEADER_RECC_REFRESH_TOKEN] = 'True';
    return {headers} as AxiosRequestConfig;
  }

  private async requestRefreshToken() {
    const result = await this.axios.post<RefreshTokenA>(
      PATH_TOKEN_REFRESH,
      undefined,
      this.refreshConfig,
    );
    return result.data.access;
  }

  private async onResponseRejected(error: AxiosError) {
    if (typeof error === 'undefined') {
      throw new Error('Undefined error object');
    }
    if (!error.response) {
      throw new Error('Undefined error.response object');
    }

    // [IMPORTANT]
    // When requesting a refresh-token,
    // it should not be handled by the main interceptor logic.
    if (error.config.headers[HEADER_RECC_REFRESH_TOKEN]) {
      return Promise.reject(error);
    }

    const status = error.response.status;
    if (status === STATUS_CODE_UNINITIALIZED_SERVICE) {
      if (this.logging) {
        console.error('Uninitialized service error');
      }
      if (this.onUninitializedService) {
        this.onUninitializedService();
      }
      throw new UninitializedServiceError();
    }

    if (status === STATUS_CODE_UNAUTHORIZED) {
      const originalConfig = error.config;
      if (this.refreshing) {
        return new Promise((resolve, reject) => {
          if (this.onRegisterRefreshSubscribers) {
            this.onRegisterRefreshSubscribers(originalConfig);
          }
          this.refreshSubscribers.push((access?: string) => {
            if (this.onUnregisterRefreshSubscribers) {
              this.onUnregisterRefreshSubscribers(originalConfig);
            }
            if (access) {
              originalConfig.headers[HEADER_AUTHORIZATION] = `Bearer ${access}`;
              resolve(this.axios(originalConfig));
            } else {
              reject(new RefreshTokenError());
            }
          });
        });
      } else {
        this.refreshing = true;
        if (this.logging) {
          console.debug('Refreshing access token ...');
        }

        let accessToken;
        try {
          accessToken = await this.requestRefreshToken();
        } catch (error) {
          if (this.logging) {
            console.error('Refresh token error');
          }
          if (this.onRefreshTokenError) {
            this.onRefreshTokenError();
          }
          this.rejectRefreshSubscribers();
          throw new RefreshTokenError();
        }

        this.setAccessToken(accessToken);

        if (this.logging) {
          console.info('Access token renewal successful');
        }
        if (this.onRenewalAccessToken) {
          this.onRenewalAccessToken(accessToken);
        }
        this.resolveRefreshSubscribers(accessToken);

        // Retry the failed request.
        originalConfig.headers[HEADER_AUTHORIZATION] = `Bearer ${accessToken}`;
        return this.axios(originalConfig);
      }
    }

    return Promise.reject(error);
  }

  resolveRefreshSubscribers(accessToken: string) {
    this.emitRefreshSubscribers(accessToken);
  }

  rejectRefreshSubscribers() {
    this.emitRefreshSubscribers(undefined);
  }

  emitRefreshSubscribers(accessToken?: string) {
    this.refreshing = false;
    const subscribers = this.refreshSubscribers;
    this.refreshSubscribers = [];
    subscribers.map(cb => cb(accessToken));
  }

  get base() {
    return this.axios.defaults.baseURL;
  }

  get origin() {
    return this.originAddress;
  }

  set origin(origin: string) {
    this.originAddress = origin;
    this.axios.defaults.baseURL = originToBaseUrl(this.originAddress, this.apiVersion);
  }

  get version() {
    return this.apiVersion;
  }

  set version(version: number) {
    this.apiVersion = version;
    this.axios.defaults.baseURL = originToBaseUrl(this.originAddress, this.apiVersion);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  get<T = any>(url: string, config?: AxiosRequestConfig) {
    return this.axios.get<T>(url, config).then(res => {
      return res.data;
    });
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.axios.post<T>(url, data, config).then(res => {
      return res.data;
    });
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.axios.patch<T>(url, data, config).then(res => {
      return res.data;
    });
  }

  delete(url: string, config?: AxiosRequestConfig) {
    return this.axios.delete(url, config);
  }

  clearTokens(ignoreHeader?: boolean) {
    this.accessToken = '';
    this.refreshToken = '';
    if (!ignoreHeader) {
      delete this.axios.defaults.headers.common[HEADER_AUTHORIZATION];
    }
  }

  setTokens(access: string, refresh: string, ignoreHeader?: boolean) {
    this.accessToken = access;
    this.refreshToken = refresh;
    if (!ignoreHeader) {
      this.axios.defaults.headers.common[HEADER_AUTHORIZATION] = `Bearer ${access}`;
    }
  }

  setAccessToken(access: string, ignoreHeader?: boolean) {
    this.accessToken = access;
    if (!ignoreHeader) {
      this.axios.defaults.headers.common[HEADER_AUTHORIZATION] = `Bearer ${access}`;
    }
  }

  static encryptPassword(password: string): string {
    return sha256hex(password);
  }

  encryptPassword(password: string): string {
    return sha256hex(password);
  }
}

export default ReccApiBase;
