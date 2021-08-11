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

    code: number;
    reason: string;
    data: any;

    constructor(response: AxiosResponse) {
        const code = response.status;
        const reason = response.statusText;
        const data = response.data;

        super(`Error: Status(${code}) ${reason}`);

        this.code = code;
        this.reason = reason;
        this.data = data;
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

export interface UpdatePassword {
    before?: string;
    after?: string;
}

export interface Extra {
    dark?: boolean;
    lang?: string;
}

export interface User {
    username?: string;
    password?: string;
    nickname?: string;
    email?: string;
    phone1?: string;
    phone2?: string;
    is_admin?: boolean;
    extra?: Extra;
    created_at?: string;
    updated_at?: string;
    last_login?: string;
}

export interface Info {
    key?: string;
    value?: string;
    created_at?: string;
    updated_at?: string;
}

export interface UpdateInfo {
    key?: string;
    value?: string;
}

export interface Login {
    access?: string;
    refresh?: string;
    user?: User;
}

export interface Project {
    name?: string;
    description?: string;
    features?: object;
    extra?: object;
    created_at?: string;
    updated_at?: string;
}

export interface SystemOverview {
    users?: number;
    groups?: number;
    projects?: number;
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

    get<T = any>(url: string, config?: AxiosRequestConfig) {
        return this.api.get(url, config)
            .then((response: AxiosResponse) => {
                if (response.status !== 200) {
                    throw new ApiV2StatusError(response);
                }
                return response.data as T;
            });
    }

    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
        return this.api.post(url, data, config)
            .then((response: AxiosResponse) => {
                if (response.status !== 200) {
                    throw new ApiV2StatusError(response);
                }
                return response.data as T;
            });
    }

    patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
        return this.api.patch(url, data, config)
            .then((response: AxiosResponse) => {
                if (response.status !== 200) {
                    throw new ApiV2StatusError(response);
                }
                return response.data as T;
            });
    }

    delete<T = any>(url: string, config?: AxiosRequestConfig) {
        return this.api.delete(url, config)
            .then((response: AxiosResponse) => {
                if (response.status !== 200) {
                    throw new ApiV2StatusError(response);
                }
                return response.data as T;
            });
    }

    // ------
    // Public
    // ------

    getVersion() {
        return this.get<string>('/public/version');
    }

    getHeartbeat() {
        return this.get('/public/heartbeat');
    }

    getTestInit() {
        return this.get<boolean>('/public/test/init');
    }

    encryptPassword(password: string): string {
        return sha256(password);
    }

    signin(username: string, password: string, updateDefaultAuth = true) {
        const auth = {
            username: username,
            password: sha256(password),
        } as AxiosBasicCredentials;

        const config = {
            auth: auth,
        } as AxiosRequestConfig;

        return this.api.post('/public/signin', undefined, config)
            .then((response: AxiosResponse) => {
                if (response.status !== 200) {
                    throw new ApiV2StatusError(response);
                }

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
            });
    }

    // ----
    // Self
    // ----

    getSelf() {
        return this.get<User>('/self');
    }

    getSelfExtra() {
        return this.get<Extra>('/self/extra');
    }

    patchSelfExtra(extra: Extra) {
        return this.patch('/self/extra', extra);
    }

    patchSelfPassword(update_password: UpdatePassword) {
        return this.patch('/self/password', update_password);
    }

    // -----
    // Infos
    // -----

    getInfos() {
        return this.get<Array<Info>>('/infos');
    }

    postInfos(info: UpdateInfo) {
        return this.post('/infos', info);
    }

    deleteInfo(key: string) {
        return this.delete(`/infos/${key}`);
    }

    // ------
    // System
    // ------

    getSystemOverview() {
        return this.get<SystemOverview>('/system/overview');
    }

    // -----
    // Users
    // -----

    getUsers() {
        return this.get<Array<User>>('/users');
    }

    postUsers(user: User) {
        return this.post('/users', user);
    }

    patchUsersUser(username: string, patchUser?: User) {
        return this.patch(`/users/${username}`, patchUser);
    }

    // --------
    // Projects
    // --------

    getProjects() {
        return this.get<Array<Project>>('/projects');
    }
}
