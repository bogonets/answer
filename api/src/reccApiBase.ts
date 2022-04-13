import AxiosLib, {AxiosInstance, AxiosRequestConfig, AxiosError} from 'axios';
import {sha256hex} from '@/crypto';
import {newUserA} from '@/packet/user';
import {newPreference} from '@/packet/preference';
import type {PreferenceA} from '@/packet/preference';
import type {UserA, SigninA, RefreshTokenA} from '@/packet/user';

const DEFAULT_TIMEOUT_MILLISECONDS = 30 * 1000;
const STATUS_CODE_ACCESS_TOKEN_ERROR = 461;
const STATUS_CODE_REFRESH_TOKEN_ERROR = 462;
const STATUS_CODE_UNINITIALIZED_SERVICE = 561;
const VALIDATE_STATUS = [200];
const HEADER_AUTHORIZATION = 'Authorization';
const PATH_TOKEN_REFRESH = '/public/token/refresh';
const DEFAULT_API_VERSION = 2;
const DEFAULT_ACCEPT = 'application/json';

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

  onAccessTokenError?: () => void;
  onRefreshTokenError?: () => void;
  onRenewalAccessToken?: (accessToken: string) => void;
  onUninitializedService?: () => void;
}

export class ReccApiBase {
  originAddress: string;
  validateStatus: Array<number>;
  apiVersion: number;
  logging: boolean;

  onAccessTokenError?: () => void;
  onRefreshTokenError?: () => void;
  onRenewalAccessToken?: (accessToken: string) => void;
  onUninitializedService?: () => void;

  session: SigninA;
  axios: AxiosInstance;

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  refreshSubscribers = [] as Array<(access: string) => any>;
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
    this.onAccessTokenError = options?.onAccessTokenError;
    this.onRefreshTokenError = options?.onRefreshTokenError;
    this.onRenewalAccessToken = options?.onRenewalAccessToken;
    this.onUninitializedService = options?.onUninitializedService;

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

  get baseURL() {
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

  async onResponseRejected(error: AxiosError) {
    if (!error.response) {
      return Promise.reject(new Error('Undefined response object'));
    }

    const status = error.response.status;
    if (status === STATUS_CODE_REFRESH_TOKEN_ERROR) {
      if (this.onAccessTokenError) {
        this.onAccessTokenError();
        // clearSession();
        // moveTo(rootNames.signin);
      }
      return Promise.reject(new Error('Expired refresh token'));
    }

    if (status === STATUS_CODE_UNINITIALIZED_SERVICE) {
      if (this.onUninitializedService) {
        this.onUninitializedService();
        // clearSession();
        // moveTo(rootNames.init);
      }
      return Promise.reject(new Error('Uninitialized service'));
    }

    if (status === STATUS_CODE_ACCESS_TOKEN_ERROR) {
      const originalConfig = error.config;

      if (this.refreshing) {
        return new Promise((resolve, reject) => {
          this.refreshSubscribers.push((access?: string) => {
            if (access) {
              originalConfig.headers.Authorization = `Bearer ${access}`;
              resolve(this.axios(originalConfig));
            } else {
              reject(new Error('Refresh token error'));
            }
          });
        });
      } else {
        this.refreshing = true;

        try {
          const refreshTokenConfig = {
            headers: {Authorization: `Bearer ${this.session.refresh}`},
          } as AxiosRequestConfig;

          if (this.logging) {
            console.debug('Refreshing access token ...');
          }
          const refreshTokenResult = await this.axios.post<RefreshTokenA>(
            PATH_TOKEN_REFRESH,
            undefined,
            refreshTokenConfig,
          );
          const access = refreshTokenResult.data.access;

          originalConfig.headers[HEADER_AUTHORIZATION] = `Bearer ${access}`;
          if (this.onRenewalAccessToken) {
            this.onRenewalAccessToken(access);
            // renewalAccessToken(access);
          }
          this.setDefaultAccessToken(access);
          if (this.logging) {
            console.info('Access token renewal successful');
          }

          this.refreshing = false;
          const subscribers = this.refreshSubscribers;
          this.refreshSubscribers = [];
          subscribers.map(cb => cb(access));

          // Retry the failed request.
          return this.axios(originalConfig);
        } catch (error) {
          if (this.logging) {
            console.error(`Refresh token error: ${error}`);
          }

          this.refreshing = false;
          const subscribers = this.refreshSubscribers;
          this.refreshSubscribers = [];
          subscribers.map(cb => cb(undefined));

          if (this.onRefreshTokenError) {
            this.onRefreshTokenError();
            // clearSession();
            // moveTo(rootNames.signin);
          }
          return Promise.reject(error);
        }
      }
    }

    return Promise.reject(error);
  }

  clearDefaultSession() {
    this.session.access = '';
    this.session.refresh = '';
    this.session.user = newUserA();
    this.session.preference = newPreference();
    delete this.axios.defaults.headers.common[HEADER_AUTHORIZATION];
  }

  setDefaultSession(
    access: string,
    refresh: string,
    user: UserA,
    preference: PreferenceA,
  ) {
    this.session.access = access;
    this.session.refresh = refresh;
    this.session.user = user;
    this.session.preference = preference;
    this.axios.defaults.headers.common[HEADER_AUTHORIZATION] = `Bearer ${access}`;
  }

  setDefaultAccessToken(access: string) {
    this.session.access = access;
    this.axios.defaults.headers.common[HEADER_AUTHORIZATION] = `Bearer ${access}`;
  }

  static encryptPassword(password: string): string {
    return sha256hex(password);
  }
}

export default ReccApiBase;
