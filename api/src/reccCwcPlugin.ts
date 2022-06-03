import ReccApi from './reccApi';
import type {ReccApiOptions} from './reccApiBase';
import type {ReccCwcDataInit, ReccCwcMessage} from './reccCwc';
import {ReccCwcOriginMismatchError, UninitializedError} from './error';
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
      this._initPromiseResolve(true);
    } catch (error) {
      this._initPromiseReject(error);
    }

    this._dark = data.dark;
    this._lang = data.lang;
    this._group = data.group || '';
    this._project = data.project || '';

    if (this._options.onInit) {
      this._options.onInit(data);
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

  get api(): ReccApi {
    if (!this._api) {
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

  toastSuccess(message: string, detail?: string) {
    postToast(this._window, {
      level: ToastLevel.Success,
      message: message,
      detail: detail,
    });
  }

  toastInfo(message: string, detail?: string) {
    postToast(this._window, {
      level: ToastLevel.Info,
      message: message,
      detail: detail,
    });
  }

  toastWarning(message: string, detail?: string) {
    postToast(this._window, {
      level: ToastLevel.Warning,
      message: message,
      detail: detail,
    });
  }

  toastError(message: string, detail?: string) {
    postToast(this._window, {
      level: ToastLevel.Error,
      message: message,
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
