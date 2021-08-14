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

export interface Signup {
    username: string;
    password: string;
    nickname?: string;
    email?: string;
    phone1?: string;
    phone2?: string;
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
    key: string;
    value: string;
    created_at: string;
    updated_at: string;
}

export interface UpdateInfo {
    key: string;
    value: string;
}

export interface UpdateInfoValue {
    value: string;
}

export interface TemplateKey {
    position: number;
    category: string;
    name: string;
}

export interface Config {
    key: string;
    type: string;
    value: string;
}

export interface UpdateConfigValue {
    value: string;
}

export interface Login {
    access: string;
    refresh: string;
    user: User;
}

export interface Group {
    name?: string;
    nickname?: string;
    description?: string;
    features?: Array<string>;
    extra?: object;
    created_at?: string;
    updated_at?: string;
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
    users: number;
    groups: number;
    projects: number;
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
            validateStatus: (status: number): boolean => {
                return status === 200;
            }
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
        return this.api.get<T>(url, config).then((res) => {
            return res.data;
        });
    }

    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
        return this.api.post<T>(url, data, config).then((res) => {
            return res.data;
        });
    }

    patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
        return this.api.patch<T>(url, data, config).then((res) => {
            return res.data;
        });
    }

    delete(url: string, config?: AxiosRequestConfig) {
        return this.api.delete(url, config);
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

    already() {
        return this.get<boolean>('/public/state/already');
    }

    encryptPassword(password: string): string {
        return sha256(password);
    }

    signup(user: Signup) {
        return this.post('/public/signup', user);
    }

    signupAdmin(user: Signup) {
        return this.post('/public/signup/admin', user);
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

    // -------
    // Configs
    // -------

    getConfigs() {
        return this.get<Array<Config>>('/configs');
    }

    patchConfig(key: string, value: string) {
        const data = {
            value: value
        } as UpdateConfigValue;
        return this.patch(`/configs/${key}`, data);
    }

    // -----
    // Infos
    // -----

    getInfos() {
        return this.get<Array<Info>>('/infos');
    }

    postInfos(key: string, value: string) {
        const data = {
            key: key,
            value: value,
        } as UpdateInfo;
        return this.post('/infos', data);
    }

    patchInfo(key: string, value: string) {
        const data = {
            value: value
        } as UpdateInfoValue;
        return this.patch(`/infos/${key}`, data);
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

    postUsers(body: User) {
        return this.post('/users', body);
    }

    patchUsersUser(username: string, body?: User) {
        return this.patch(`/users/${username}`, body);
    }

    deleteUsersUser(username: string) {
        return this.delete(`/users/${username}`);
    }

    // ---------
    // Templates
    // ---------

    getTemplates() {
        return this.get<Array<TemplateKey>>(`/templates`);
    }

    // -----
    // Groups
    // -----

    getGroups() {
        return this.get<Array<Group>>('/groups');
    }

    postGroups(body: Group) {
        return this.post('/groups', body);
    }

    patchGroupsGroup(name: string, body?: Group) {
        return this.patch(`/users/${name}`, body);
    }

    deleteGroupsGroup(group: string) {
        return this.delete(`/users/${group}`);
    }

    // --------
    // Projects
    // --------

    getProjects() {
        return this.get<Array<Project>>('/projects');
    }
}
