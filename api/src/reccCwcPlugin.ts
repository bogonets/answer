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

  unregister() {
    this._window.removeEventListener(MESSAGE_EVENT_TYPE, this._messageHandler);
  }

  runDebuggingMode() {
    if (process.env.NODE_ENV !== 'production') {
      (async () => {
        await this.debug();
      })();
    }
  }

  async debug() {
    if (process.env.NODE_ENV === 'production') {
      throw new UnsupportedOperationError(
        'Debug operations are not supported in production mode',
      );
    }

    const envs = debugEnvs();
    const api = new ReccApi({origin: envs.apiOrigin});
    const signin = await api.postSignin(envs.username, envs.password);
    const accessToken = signin.access;
    const refreshToken = signin.refresh;

    this.onInit({
      apiOptions: {accessToken, refreshToken},
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
      return api.post<T>(url, config);
    });
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.waitInitialized().then(api => {
      return api.patch<T>(url, config);
    });
  }

  delete(url: string, config?: AxiosRequestConfig) {
    return this.waitInitialized().then(api => {
      return api.delete(url, config);
    });
  }

  toastSuccess(message: string, detail?: string) {
    postToast(this._window, {level: ToastLevel.Success, message, detail});
  }

  toastInfo(message: string, detail?: string) {
    postToast(this._window, {level: ToastLevel.Info, message, detail});
  }

  toastWarning(message: string, detail?: string) {
    postToast(this._window, {level: ToastLevel.Warning, message, detail});
  }

  toastError(message: string, detail?: string) {
    postToast(this._window, {level: ToastLevel.Error, message, detail});
  }

  toastRequestSuccess(detail?: string) {
    postToast(this._window, {level: ToastLevel.RequestSuccess, detail});
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

    postToast(this._window, {
      level: ToastLevel.RequestFailure,
      detail: detail,
    });
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
