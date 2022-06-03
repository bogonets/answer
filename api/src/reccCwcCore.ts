import type {ReccApiOptions} from './reccApiBase';
import type {
  ReccCwcDataFullscreen,
  ReccCwcDataMove,
  ReccCwcDataRenewalAccessToken,
  ReccCwcDataToast,
  ReccCwcMessage,
} from './reccCwc';
import {UninitializedError, ReccCwcOriginMismatchError} from './error';
import {
  MESSAGE_EVENT_TYPE,
  MESSAGE_DATA_TYPE_TOAST,
  MESSAGE_DATA_TYPE_MOVE,
  MESSAGE_DATA_TYPE_FULLSCREEN,
  MESSAGE_DATA_TYPE_REFRESH_TOKEN_ERROR,
  MESSAGE_DATA_TYPE_RENEWAL_ACCESS_TOKEN,
  MESSAGE_DATA_TYPE_UNINITIALIZED_SERVICE,
  postInit,
} from './reccCwc';

export interface ReccCwcCoreOptions {
  origin?: string;

  onToast?: (data: ReccCwcDataToast) => void;
  onMove?: (data: ReccCwcDataMove) => void;
  onFullscreen?: (data: ReccCwcDataFullscreen) => void;

  onRefreshTokenError?: () => void;
  onRenewalAccessToken?: (data: ReccCwcDataRenewalAccessToken) => void;
  onUninitializedService?: () => void;
}

/**
 * Cross-window communication for RECC Core.
 */
export class ReccCwcCore {
  _messageHandler: (event: MessageEvent<ReccCwcMessage>) => void;
  _options: ReccCwcCoreOptions;
  _window: Window;

  constructor(frame: HTMLIFrameElement, options?: ReccCwcCoreOptions) {
    this._messageHandler = (event: MessageEvent<ReccCwcMessage>) => {
      this.onMessage(event);
    };

    if (!frame.contentWindow) {
      throw new UninitializedError('The frame window does not exist');
    }

    this._options = options ?? {};
    this._window = frame.contentWindow;
    this._window.addEventListener(MESSAGE_EVENT_TYPE, this._messageHandler);
  }

  unregister() {
    this._window.removeEventListener(MESSAGE_EVENT_TYPE, this._messageHandler);
  }

  onMessage(event: MessageEvent<ReccCwcMessage>) {
    if (this._options.origin) {
      if (this._options.origin !== event.origin) {
        throw new ReccCwcOriginMismatchError();
      }
    }

    switch (event.data.type) {
      case MESSAGE_DATA_TYPE_TOAST:
        if (this._options.onToast) {
          this._options.onToast(event.data.data as ReccCwcDataToast);
        }
        break;

      case MESSAGE_DATA_TYPE_MOVE:
        if (this._options.onMove) {
          this._options.onMove(event.data.data as ReccCwcDataMove);
        }
        break;

      case MESSAGE_DATA_TYPE_FULLSCREEN:
        if (this._options.onFullscreen) {
          this._options.onFullscreen(event.data.data as ReccCwcDataFullscreen);
        }
        break;

      case MESSAGE_DATA_TYPE_REFRESH_TOKEN_ERROR:
        if (this._options.onRefreshTokenError) {
          this._options.onRefreshTokenError();
        }
        break;

      case MESSAGE_DATA_TYPE_RENEWAL_ACCESS_TOKEN:
        if (this._options.onRenewalAccessToken) {
          this._options.onRenewalAccessToken(
            event.data.data as ReccCwcDataRenewalAccessToken,
          );
        }
        break;

      case MESSAGE_DATA_TYPE_UNINITIALIZED_SERVICE:
        if (this._options.onUninitializedService) {
          this._options.onUninitializedService();
        }
        break;
    }
  }

  postInit(apiOptions: ReccApiOptions, dark: boolean, lang: string) {
    postInit(this._window, {apiOptions, dark, lang});
  }
}

export default ReccCwcCore;
