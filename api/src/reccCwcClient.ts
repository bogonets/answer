import type {AxiosRequestConfig} from 'axios';
import ReccApi from './reccApi';
import type {ReccApiOptions} from './reccApiBase';
import type {ReccCwcDataInit, ReccCwcMessage} from './reccCwc';
import {
  IllegalArgumentError,
  ReccCwcOriginMismatchError,
  TimeoutError,
  UninitializedError,
} from './error';
import {
  MESSAGE_EVENT_TYPE,
  MESSAGE_DATA_TYPE_INIT,
  ToastLevel,
  postToast,
  postMove,
  postFullscreen,
  postRefreshTokenError,
  postRenewalAccessToken,
  postUninitializedService,
} from './reccCwc';

export interface ReccCwcClientOptions {
  origin?: string;
  onInit?: (data: ReccCwcDataInit) => void;
}

export interface ReccCwcClientInit {
  origin: string;
  username: string;
  password: string;
  dark: number;
  lang: string;
  timezone: string;
  group: string;
  project: string;
}

function debugEnvs(): ReccCwcClientInit {
  const origin = process.env.RECC_CWC_CLIENT_ORIGIN || 'http://localhost:20000';
  const username = process.env.RECC_CWC_CLIENT_USERNAME || 'admin';
  const password = process.env.RECC_CWC_CLIENT_PASSWORD || '0000';
  const darkText = process.env.RECC_CWC_CLIENT_DARK;
  const dark = darkText ? Number.parseInt(darkText) : 0;
  const lang = process.env.RECC_CWC_CLIENT_LANG || 'ko';
  const timezone = process.env.RECC_CWC_CLIENT_TIMEZONE || 'Asia/Seoul';
  const group = process.env.RECC_CWC_CLIENT_GROUP || 'group';
  const project = process.env.RECC_CWC_CLIENT_PROJECT || 'project';

  return {
    origin,
    username,
    password,
    dark,
    lang,
    timezone,
    group,
    project,
  } as ReccCwcClientInit;
}

/**
 * Cross-window communication for RECC Plugin.
 */
export class ReccCwcClient {
  _messageHandler: (event: MessageEvent<ReccCwcMessage>) => void;

  _options: ReccCwcClientOptions;
  _window: Window;

  _api?: ReccApi = undefined;
  _dark = 0;
  _lang = 'en';
  _timezone = '';
  _group = '';
  _project = '';

  _initPromise: Promise<boolean>;
  _initPromiseResolve: (value: boolean) => void;
  _initPromiseReject: (reason: string) => void;

  constructor(window: Window, options?: ReccCwcClientOptions) {
    this._messageHandler = (event: MessageEvent<ReccCwcMessage>) => {
      this.onMessage(event);
    };
    this._options = options ?? {};
    this._window = window;
    this._window.addEventListener(MESSAGE_EVENT_TYPE, this._messageHandler);

    this._initPromise = new Promise((resolve, reject) => {
      this._initPromiseResolve = resolve;
      this._initPromiseReject = reject;
    });
  }

  asParamsText() {
    let result = '';
    if (this.origin) {
      result = `api='${this.origin}',`;
    }
    if (this.group) {
      result += `group='${this.group}',`;
    }
    if (this.project) {
      result += `project='${this.project}',`;
    }
    if (this.lang) {
      result += `lang='${this.lang}',`;
    }
    if (this.timezone) {
      result += `timezone='${this.timezone}',`;
    }
    return result + `dark=${this.dark}`;
  }

  toString() {
    return `ReccCwcClient(${this.asParamsText()})`;
  }

  unregister() {
    this._window.removeEventListener(MESSAGE_EVENT_TYPE, this._messageHandler);
  }

  async init(options = debugEnvs()) {
    const api = new ReccApi({origin: options.origin});
    await api.postSignin(options.username, options.password);

    // `onInit()` is a message received from the parent window.
    // Debugging mode forces this message to occur.
    this.onInit({
      apiOptions: api.asPortableOptions(),
      dark: options.dark,
      lang: options.lang,
      timezone: options.timezone,
      group: options.group,
      project: options.project,
    });
  }

  onInit(data: ReccCwcDataInit) {
    const apiOptions = {
      ...data.apiOptions,

      onRefreshTokenError: () => {
        postRefreshTokenError(this._window);
      },
      onRenewalAccessToken: (accessToken: string) => {
        postRenewalAccessToken(this._window, {accessToken});
      },
      onUninitializedService: () => {
        postUninitializedService(this._window);
      },
    } as ReccApiOptions;

    try {
      this._api = new ReccApi(apiOptions);

      this._dark = data.dark;
      this._lang = data.lang;
      this._timezone = data.timezone;

      this._group = data.group || '';
      this._project = data.project || '';

      if (this._options.onInit) {
        this._options.onInit(data);
      }

      this._initPromiseResolve(true);
    } catch (error) {
      this._initPromiseReject(error);
    }
  }

  onMessage(event: MessageEvent<ReccCwcMessage>) {
    if (this._options.origin) {
      if (this._options.origin !== event.origin) {
        throw new ReccCwcOriginMismatchError();
      }
    }

    switch (event.data.type) {
      case MESSAGE_DATA_TYPE_INIT:
        this.onInit(event.data.data as ReccCwcDataInit);
        break;
    }
  }

  waitInitialized(timeout?: number) {
    const initPromise = this._initPromise.then((value: boolean) => {
      if (!value) {
        throw new Error();
      }
      return this.api;
    });

    if (typeof timeout !== 'undefined') {
      return initPromise;
    }

    const timeoutPromise = new Promise((resolve, reject) => {
      setTimeout(() => {
        reject(new TimeoutError('An initialization timeout occurred'));
      }, timeout);
    });

    return Promise.race([initPromise, timeoutPromise]);
  }

  get initialized(): boolean {
    return typeof this._api !== 'undefined';
  }

  get api(): ReccApi {
    if (!this.initialized) {
      throw new UninitializedError();
    }
    return this._api;
  }

  get origin() {
    return this.api.origin;
  }

  get dark() {
    return this._dark;
  }

  get isLight() {
    return this._dark === 0;
  }

  get isDark() {
    return this._dark === 1;
  }

  get lang() {
    return this._lang;
  }

  get timezone() {
    return this._timezone;
  }

  get group() {
    return this._group;
  }

  get project() {
    return this._project;
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  get<T = any>(url: string, config?: AxiosRequestConfig) {
    return this.api.get<T>(url, config);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.api.post<T>(url, data, config);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.api.patch<T>(url, data, config);
  }

  delete(url: string, config?: AxiosRequestConfig) {
    return this.api.delete(url, config);
  }

  getPluginPrefix(name: string, withGroup = true, withProject = true) {
    if (withGroup && withProject) {
      return `/plugins/${name}/${this._group}/${this._project}`;
    } else if (withGroup && !withProject) {
      return `/plugins/${name}/${this._group}`;
    } else if (!withGroup && withProject) {
      throw new IllegalArgumentError('A project cannot be assigned without a group');
    } else {
      console.assert(!withGroup);
      console.assert(!withProject);
      return `/plugins/${name}`;
    }
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toast(level: ToastLevel, message?: any, detail?: any) {
    let m: string | undefined;
    if (typeof message !== 'undefined') {
      if (typeof message === 'string') {
        m = message;
      } else {
        m = message.toString();
      }
    }

    let d: string | undefined;
    if (typeof detail !== 'undefined') {
      if (typeof detail === 'string') {
        d = detail;
      } else {
        d = detail.toString();
      }
    }

    postToast(this._window, {level: level, message: m, detail: d});
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toastSuccess(message: any, detail?: any) {
    this.toast(ToastLevel.Success, message, detail);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toastInfo(message: any, detail?: any) {
    this.toast(ToastLevel.Info, message, detail);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toastWarning(message: any, detail?: any) {
    this.toast(ToastLevel.Warning, message, detail);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toastError(message: any, detail?: any) {
    this.toast(ToastLevel.Error, message, detail);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toastRequestSuccess(detail?: any) {
    this.toast(ToastLevel.RequestSuccess, undefined, detail);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  toastRequestFailure(error?: any) {
    let detail: undefined | string = undefined;
    if (error) {
      if (typeof error.response !== 'undefined') {
        const code = error.response.status || '?';
        const reason = error.response.statusText || 'Unknown';
        detail = `[${code}] ${reason}`;
      } else {
        detail = error.toString();
      }
    }

    this.toast(ToastLevel.RequestFailure, undefined, detail);
  }

  moveToName(name: string, params?: object) {
    postMove(this._window, {name, params});
  }

  moveToPath(path: string, params?: object) {
    postMove(this._window, {path, params});
  }

  flipFullscreenMode() {
    postFullscreen(this._window, {flip: true});
  }

  fullscreenMode(flag: boolean) {
    postFullscreen(this._window, {fullscreen: flag});
  }
}

export default ReccCwcClient;
