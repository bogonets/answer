import AxiosLib, {
    AxiosInstance,
    AxiosPromise,
    AxiosResponse,
    AxiosRequestConfig,
    AxiosBasicCredentials,
} from 'axios'
import sha256 from 'sha256'

const DEFAULT_PROTOCOL = document.location.protocol;
const DEFAULT_HOST = document.location.host;
const DEFAULT_ORIGIN = document.location.origin;

const DEFAULT_TIMEOUT = 30 * 1000;

export class ApiV2ResponseError extends Error {
    constructor(response: AxiosResponse) {
        const code = response.status;
        const text = response.statusText;
        super(`Error: Status(${code}) ${text}`);
    }
}

export function originToBaseUrl(origin: string): string {
    if (origin[origin.length-1] == '/') {
        return origin + 'api/v2';
    } else {
        return origin + '/api/v2';
    }
}

export interface Login {
    access?: string;
    refresh?: string;
}

export default class ApiV2 {

    private _origin: string;
    private _api: AxiosInstance;

    constructor(
        origin: string = DEFAULT_ORIGIN,
        timeout: number = DEFAULT_TIMEOUT,
    ) {
        this._origin = origin;
        this._api = AxiosLib.create({
            baseURL: originToBaseUrl(origin),
            timeout: timeout,
        });
    }

    get baseURL(): string {
        if (this._api.defaults.baseURL) {
            return this._api.defaults.baseURL;
        } else {
            return '';
        }
    }

    get origin(): string {
        return this._origin;
    }

    set origin(origin: string) {
        this._origin = origin;
        this._api.defaults.baseURL = originToBaseUrl(origin);
    }

    setDefaultBearerAuthorization(token: string) {
        this._api.defaults.headers['Authorization'] = `Bearer ${token}`;
    }

    async version(): Promise<string> {
        return await this._api.get('/public/version')
            .then(response => {
                return response.data;
            })
            .catch(error => {
                console.debug(error);
                // EMPTY.
            });
    }

    heartbeat() {
        return this._api.get('/public/heartbeat');
    }

    testInit() {
        return this._api.get('/public/test/init');
    }

    login(username: string, password: string, updateDefaultAuth = true) {
        const auth = {
            username: username,
            password: sha256(password),
        } as AxiosBasicCredentials;
        const config = {
            auth: auth,
            headers: {
                Accept: 'application/json',
            },
        } as AxiosRequestConfig;
        return this._api.post('/public/login', undefined, config)
            .then((response: AxiosResponse) => {
                if (response.status == 200) {
                    const result = response.data as Login;
                    if (updateDefaultAuth) {
                        const access = result.access ? result.access : '';
                        this.setDefaultBearerAuthorization(access);
                    }
                    return result;
                } else {
                    throw new ApiV2ResponseError(response);
                }
            });
    }
}
