import AxiosLib, {
    AxiosInstance,
    AxiosResponse,
    AxiosRequestConfig,
    AxiosBasicCredentials,
} from 'axios'
import sha256 from 'sha256'

const DEFAULT_ORIGIN = document.location.origin;
const DEFAULT_TIMEOUT = 30 * 1000;

export class ApiV2StatusError extends Error {
    constructor(code: number, reason: string) {
        super(`Error: Status(${code}) ${reason}`);
    }
}

export class ApiV2TokenError extends Error {
    constructor(token?: string) {
        let message;
        if (token) {
            message = `Invalid token error: ${token}`;
        } else {
            message = 'Empty token error';
        }
        super(message);
    }
}

export class ApiV2AccessTokenError extends ApiV2TokenError {
    constructor(token?: string) {
        super(token);
    }
}

export class ApiV2RefreshTokenError extends ApiV2TokenError {
    constructor(token?: string) {
        super(token);
    }
}

export function originToBaseUrl(origin: string): string {
    if (origin[origin.length-1] == '/') {
        return origin + 'api/v2';
    } else {
        return origin + '/api/v2';
    }
}

export interface Extra {
    dark?: boolean;
    lang?: string;
}

export interface User {
    username?: string;
    email?: string;
    phone1?: string;
    phone2?: string;
    is_admin?: boolean;
    extra?: Extra;
    created_at?: string;
    updated_at?: string;
    last_login?: string;
}

export interface Login {
    access?: string;
    refresh?: string;
    user?: User;
}

function newEmptySession(): Login {
    return {
        access: '',
        refresh: '',
        user: {
            username: '',
            email: '',
            phone1: '',
            phone2: '',
            is_admin: false,
            extra: {
                dark: false,
                lang: '',
            } as Extra,
            created_at: '',
            updated_at: '',
            last_login: '',
        } as User,
    } as Login;
}

export default class ApiV2 {

    private originAddress: string;
    private api: AxiosInstance;
    private session: Login;

    constructor(
        origin: string = DEFAULT_ORIGIN,
        timeout: number = DEFAULT_TIMEOUT,
    ) {
        this.originAddress = origin;
        this.api = AxiosLib.create({
            baseURL: originToBaseUrl(origin),
            timeout: timeout,
            headers: {
                Accept: 'application/json',
            },
        });
        this.session = newEmptySession();
    }

    get baseURL(): string {
        if (this.api.defaults.baseURL) {
            return this.api.defaults.baseURL;
        } else {
            return '';
        }
    }

    get origin(): string {
        return this.originAddress;
    }

    set origin(origin: string) {
        this.originAddress = origin;
        this.api.defaults.baseURL = originToBaseUrl(origin);
    }

    setDefaultSession(access: string, refresh: string, user: User) {
        this.session.access = access;
        this.session.refresh = refresh;
        this.session.user = user;
    }

    setDefaultBearerAuthorization(token: string) {
        this.api.defaults.headers['Authorization'] = `Bearer ${token}`;
    }

    async version(): Promise<string> {
        return await this.api.get('/public/version')
            .then(response => {
                return response.data;
            })
            .catch(error => {
                console.debug(error);
                // EMPTY.
            });
    }

    heartbeat() {
        return this.api.get('/public/heartbeat');
    }

    testInit() {
        return this.api.get('/public/test/init');
    }

    login(username: string, password: string, updateDefaultAuth = true) {
        const auth = {
            username: username,
            password: sha256(password),
        } as AxiosBasicCredentials;
        const config = {
            auth: auth,
        } as AxiosRequestConfig;
        return this.api.post('/public/login', undefined, config)
            .then((response: AxiosResponse) => {
                if (response.status == 200) {
                    const result = response.data as Login;
                    const access = result.access;
                    const refresh = result.refresh;
                    if (!access) {
                        throw new ApiV2AccessTokenError(access);
                    }
                    if (!refresh) {
                        throw new ApiV2RefreshTokenError(refresh);
                    }
                    if (updateDefaultAuth) {
                        const user = result.user || {};
                        this.setDefaultSession(access, refresh, user);
                        this.setDefaultBearerAuthorization(access);
                    }
                    return result;
                } else {
                    const code = response.status;
                    const reason = response.statusText;
                    throw new ApiV2StatusError(code, reason);
                }
            });
    }
}
