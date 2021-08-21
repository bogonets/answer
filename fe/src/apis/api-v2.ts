import AxiosLib, {
    AxiosInstance,
    AxiosResponse,
    AxiosRequestConfig,
    AxiosBasicCredentials,
} from 'axios'
import {ConfigA, UpdateConfigValueQ} from '@/packet/config';
import {GroupA, CreateGroupQ, UpdateGroupQ} from '@/packet/group';
import {InfoA, CreateInfoQ, UpdateInfoQ} from '@/packet/info';
import {PermissionA, CreatePermissionQ, UpdatePermissionQ} from '@/packet/permission';
import {TemplateA} from '@/packet/template';
import {ProjectA, CreateProjectQ, UpdateProjectQ} from '@/packet/project';
import {SystemOverviewA} from '@/packet/system';
import {
    UserA,
    UpdateUserQ,
    SigninA,
    SignupQ,
    UpdatePasswordQ,
    UserExtra,
    createEmptySigninA,
} from '@/packet/user';
import {encryptSha256} from '@/crypto/sha';

const DEFAULT_TIMEOUT = 30 * 1000;


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

export default class ApiV2 {

    private originAddress: string;
    private api: AxiosInstance;
    private session: SigninA;

    constructor(
        origin: string = document.location.origin,
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
        this.session = createEmptySigninA();
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

    setDefaultSession(access: string, refresh: string, user: UserA) {
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

    encryptPassword(password: string): string {
        return encryptSha256(password);
    }

    // ------
    // Public
    // ------

    getHeartbeat() {
        return this.get('/public/heartbeat');
    }

    getVersion() {
        return this.get<string>('/public/version');
    }

    already() {
        return this.get<boolean>('/public/state/already');
    }

    signup(body: SignupQ) {
        return this.post('/public/signup', body);
    }

    signupAdmin(body: SignupQ) {
        return this.post('/public/signup/admin', body);
    }

    signin(username: string, password: string, updateDefaultAuth = true) {
        const auth = {
            username: username,
            password: encryptSha256(password),
        } as AxiosBasicCredentials;

        const config = {
            auth: auth,
        } as AxiosRequestConfig;

        return this.api.post('/public/signin', undefined, config)
            .then((response: AxiosResponse) => {
                const result = response.data as SigninA;
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
        return this.get<UserA>('/self');
    }

    patchSelf(body: UpdateUserQ) {
        return this.patch<UserA>('/self', body);
    }

    getSelfExtra() {
        return this.get<UserExtra>('/self/extra');
    }

    patchSelfExtra(extra: UserExtra) {
        return this.patch('/self/extra', extra);
    }

    patchSelfPassword(body: UpdatePasswordQ) {
        return this.patch('/self/password', body);
    }

    // ------
    // Self/Groups
    // ------

    getSelfGroups() {
        return this.get<Array<GroupA>>('/self/groups');
    }

    postSelfGroups(body: CreateGroupQ) {
        return this.post('/self/groups', body);
    }

    getSelfGroupsPgroup(group: string) {
        return this.get<GroupA>(`/self/groups/${group}`);
    }

    patchSelfGroupsPgroup(group: string, body: UpdateGroupQ) {
        return this.patch(`/self/groups/${group}`, body);
    }

    deleteSelfGroupsGroup(group: string) {
        return this.delete(`/self/groups/${group}`);
    }

    // --------
    // Self/Projects
    // --------

    getSelfProjects() {
        return this.get<Array<ProjectA>>('/self/projects');
    }

    postSelfProjects(body: CreateProjectQ) {
        return this.post('/self/projects', body);
    }

    getSelfProjectsPgroupPproject(group: string, project: string) {
        return this.get<ProjectA>(`/self/projects/${group}/${project}`);
    }

    patchSelfProjectsPgroupPproject(
        group: string,
        project: string,
        body: UpdateProjectQ,
    ) {
        return this.patch(`/self/projects/${group}/${project}`, body);
    }

    deleteSelfProjectsPgroupProject(group: string, project: string) {
        return this.delete(`/self/projects/${group}/${project}`);
    }

    // -------
    // Configs
    // -------

    getConfigs() {
        return this.get<Array<ConfigA>>('/configs');
    }

    getConfigsPkey(key: string) {
        return this.get<ConfigA>(`/configs/${key}`);
    }

    patchConfigsPkey(key: string, body: UpdateConfigValueQ) {
        return this.patch(`/configs/${key}`, body);
    }

    // -----
    // Infos
    // -----

    getInfos() {
        return this.get<Array<InfoA>>('/infos');
    }

    postInfos(body: CreateInfoQ) {
        return this.post('/infos', body);
    }

    getInfosPkey(key: string) {
        return this.get<InfoA>(`/infos/${key}`);
    }

    patchInfosPkey(key: string, body: UpdateInfoQ) {
        return this.patch(`/infos/${key}`, body);
    }

    deleteInfo(key: string) {
        return this.delete(`/infos/${key}`);
    }

    // ------
    // System
    // ------

    getSystemOverview() {
        return this.get<SystemOverviewA>('/system/overview');
    }

    // ---------
    // Templates
    // ---------

    getTemplates() {
        return this.get<Array<TemplateA>>(`/templates`);
    }

    // -----
    // Users
    // -----

    getUsers() {
        return this.get<Array<UserA>>('/users');
    }

    postUsers(body: SignupQ) {
        return this.post('/users', body);
    }

    getUsersPuser(user: string) {
        return this.get<UserA>(`/users/${user}`);
    }

    patchUsersPuser(user: string, body: UpdateUserQ) {
        return this.patch(`/users/${user}`, body);
    }

    deleteUsersPuser(user: string) {
        return this.delete(`/users/${user}`);
    }

    // ------
    // Groups
    // ------

    getGroups() {
        return this.get<Array<GroupA>>('/groups');
    }

    postGroups(body: CreateGroupQ) {
        return this.post('/groups', body);
    }

    getGroupsPgroup(group: string) {
        return this.get<GroupA>(`/groups/${group}`);
    }

    patchGroupsPgroup(group: string, body: UpdateGroupQ) {
        return this.patch(`/groups/${group}`, body);
    }

    deleteGroupsGroup(group: string) {
        return this.delete(`/groups/${group}`);
    }

    // --------
    // Projects
    // --------

    getProjects() {
        return this.get<Array<ProjectA>>('/projects');
    }

    postProjects(body: CreateProjectQ) {
        return this.post('/projects', body);
    }

    getProjectsPgroupPproject(group: string, project: string) {
        return this.get<ProjectA>(`/projects/${group}/${project}`);
    }

    patchProjectsPgroupPproject(group: string, project: string, body: UpdateProjectQ) {
        return this.patch(`/projects/${group}/${project}`, body);
    }

    deleteProjectsPgroupProject(group: string, project: string) {
        return this.delete(`/projects/${group}/${project}`);
    }

    // -----------
    // Permissions
    // -----------

    getPermissions() {
        return this.get<Array<PermissionA>>('/permissions');
    }

    postPermissions(body: CreatePermissionQ) {
        return this.post('/permissions', body);
    }

    getPermissionsPperm(perm: string) {
        return this.get<PermissionA>(`/permissions/${perm}`);
    }

    patchPermissionsPperm(perm: string, body: UpdatePermissionQ) {
        return this.patch(`/permissions/${perm}`, body);
    }

    deletePermissionsPperm(perm: string) {
        return this.delete(`/permissions/${perm}`);
    }
}
