import type {AxiosRequestConfig} from 'axios';
import ReccApi from './reccApi';
import type {ReccApiOptions} from './reccApiBase';
import type {ReccCwcDataInit, ReccCwcMessage} from './reccCwc';
import {
  ReccCwcOriginMismatchError,
  UninitializedError,
  UnsupportedOperationError,
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

export interface ReccCwcPluginOptions {
  origin?: string;
  onInit?: (data: ReccCwcDataInit) => void;
}

function isDebuggingMode() {
  return process.env.NODE_ENV !== 'production';
}

function debugEnvs() {
  return {
    apiOrigin: process.env.RECC_CWC_PLUGIN_DEBUG_API_ORIGIN || 'http://localhost:20000',
    username: process.env.RECC_CWC_PLUGIN_DEBUG_USERNAME || 'admin',
    password: process.env.RECC_CWC_PLUGIN_DEBUG_PASSWORD || '0000',
    dark: process.env.RECC_CWC_PLUGIN_DEBUG_DARK === 'true',
    lang: process.env.RECC_CWC_PLUGIN_DEBUG_LANG || 'ko',
    group: process.env.RECC_CWC_PLUGIN_DEBUG_GROUP || 'group',
    project: process.env.RECC_CWC_PLUGIN_DEBUG_PROJECT || 'project',
  };
}

/**
 * Cross-window communication for RECC Plugin.
 */
export class ReccCwcPlugin {
  _messageHandler: (event: MessageEvent<ReccCwcMessage>) => void;
  _options: ReccCwcPluginOptions;
  _window: Window;

  _api?: ReccApi = undefined;
  _dark = false;
  _lang = 'en';
  _group = '';
  _project = '';

  _initPromise: Promise<boolean>;
  _initPromiseResolve: (value: boolean) => void;
  _initPromiseReject: (reason: string) => void;

  constructor(window: Window, options?: ReccCwcPluginOptions) {
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

  get debuggingMode() {
    return isDebuggingMode();
  }

  asParamsText() {
    let result = '';
    if (this.apiOrigin) {
      result = `api='${this.apiOrigin}',`;
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
    return result + `dark=${this.dark}`;
  }

  toString() {
    return `ReccCwcPlugin(${this.asParamsText()})`;
  }

  unregister() {
    this._window.removeEventListener(MESSAGE_EVENT_TYPE, this._messageHandler);
  }

  async debug() {
    if (!this.debuggingMode) {
      throw new UnsupportedOperationError(
        'Debug operations are not supported in production mode',
      );
    }

    const envs = debugEnvs();
    const api = new ReccApi({origin: envs.apiOrigin});
    await api.postSignin(envs.username, envs.password);

    // `onInit()` is a message received from the parent window.
    // Debugging mode forces this message to occur.
    this.onInit({
      apiOptions: api.asPortableOptions(),
      dark: envs.dark,
      lang: envs.lang,
      group: envs.group,
      project: envs.project,
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

  waitInitialized() {
    return this._initPromise.then((value: boolean) => {
      if (!value) {
        throw new Error();
      }
      return this.api;
    });
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

  get apiOrigin() {
    return this.api.origin;
  }

  get dark() {
    return this._dark;
  }

  get lang() {
    return this._lang;
  }

  get group() {
    return this._group;
  }

  get project() {
    return this._project;
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  get<T = any>(url: string, config?: AxiosRequestConfig) {
    return this.waitInitialized().then(api => {
      return api.get<T>(url, config);
    });
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.waitInitialized().then(api => {
      return api.post<T>(url, data, config);
    });
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.waitInitialized().then(api => {
      return api.patch<T>(url, data, config);
    });
  }

  delete(url: string, config?: AxiosRequestConfig) {
    return this.waitInitialized().then(api => {
      return api.delete(url, config);
    });
  }

  getPluginPathPrefix(name: string) {
    return `/plugins/${name}/${this._group}/${this._project}`;
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

export default ReccCwcPlugin;
