import AxiosLib, { AxiosInstance, AxiosPromise } from 'axios'

const DEFAULT_PROTOCOL = document.location.protocol;
const DEFAULT_HOST = document.location.host;
const DEFAULT_ORIGIN = document.location.origin;

const DEFAULT_TIMEOUT = 30 * 1000;

export function originToBaseUrl(origin: string): string {
    if (origin[origin.length-1] == '/') {
        return origin + 'api/v2';
    } else {
        return origin + '/api/v2';
    }
}

export default class ApiV2 {

    private _api: AxiosInstance;

    constructor(
        origin: string = DEFAULT_ORIGIN,
        timeout: number = DEFAULT_TIMEOUT,
    ) {
        this._api = AxiosLib.create({
            baseURL: originToBaseUrl(origin),
            timeout: timeout,
        });
    }

    get baseURL(): string {
        if (this._api.defaults.baseURL) {
            return this._api.defaults.baseURL;
        } else {
            return "";
        }
    }

    set origin(origin: string) {
        this._api.defaults.baseURL = originToBaseUrl(origin);
    }

    async version(): Promise<string> {
        return await this._api.get("/public/version")
            .then(response => {
                return response.data;
            })
            .catch(error => {
                console.debug(error);
                // EMPTY.
            });
    }

    heartbeat() {
        return this._api.get("/public/heartbeat");
    }

    testInit() {
        return this._api.get("/public/test/init");
    }
}
