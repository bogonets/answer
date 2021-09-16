import AxiosLib from 'axios';
import type {AxiosInstance, AxiosResponse, AxiosRequestConfig, AxiosBasicCredentials} from 'axios';
import type {AirjoyDeviceA, AirjoySensorA} from '@/packet/airjoy';
import type {ConfigA, UpdateConfigValueQ} from '@/packet/config';
import type {GroupA, CreateGroupQ, UpdateGroupQ} from '@/packet/group';
import type {InfoA, CreateInfoQ, UpdateInfoQ} from '@/packet/info';
import type {PermissionA, CreatePermissionQ, UpdatePermissionQ} from '@/packet/permission';
import type {TemplateA} from '@/packet/template';
import type {ProjectA, CreateProjectQ, UpdateProjectQ} from '@/packet/project';
import type {MemberA, CreateMemberQ, UpdateMemberQ} from '@/packet/member';
import type {SystemOverviewA} from '@/packet/system';
import type {UserA, UpdateUserQ, SigninA, SignupQ, UpdatePasswordQ, UserExtra} from '@/packet/user';
import {createEmptySigninA, createEmptyUserA} from '@/packet/user';
import {PreferenceA, createEmptyPreference} from '@/packet/preference';
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

    setDefaultSession(
        access: string,
        refresh: string,
        user: UserA,
        preference: PreferenceA,
    ) {
        this.session.access = access;
        this.session.refresh = refresh;
        this.session.user = user;
        this.session.preference = preference;
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

    getPublicHeartbeat() {
        return this.get('/public/heartbeat');
    }

    getPublicVersion() {
        return this.get<string>('/public/version');
    }

    getPublicStateAlready() {
        return this.get<boolean>('/public/state/already');
    }

    postPublicSignup(body: SignupQ) {
        return this.post('/public/signup', body);
    }

    postPublicSignupAdmin(body: SignupQ) {
        return this.post('/public/signup/admin', body);
    }

    postSignin(username: string, password: string, updateDefaultAuth = true) {
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
                    const user = result.user || createEmptyUserA();
                    const preference = result.preference || createEmptyPreference();
                    this.setDefaultSession(access, refresh, user, preference);
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

    // -----------
    // Main/Groups
    // -----------

    getMainGroups() {
        return this.get<Array<GroupA>>('/main/groups');
    }

    postMainGroups(body: CreateGroupQ) {
        return this.post('/main/groups', body);
    }

    getMainGroupsPgroup(group: string) {
        return this.get<GroupA>(`/main/groups/${group}`);
    }

    patchMainGroupsPgroup(group: string, body: UpdateGroupQ) {
        return this.patch(`/main/groups/${group}`, body);
    }

    deleteMainGroupsGroup(group: string) {
        return this.delete(`/main/groups/${group}`);
    }

    // -------------------
    // Main/Groups/Members
    // -------------------

    getMainGroupsPgroupMembers(group: string) {
        return this.get<Array<MemberA>>(`/main/groups/${group}/members`);
    }

    postMainGroupsPgroupMembers(group: string, body: CreateMemberQ) {
        return this.post(`/main/groups/${group}/members`, body);
    }

    getMainGroupsPgroupMembersPmember(group: string, member: string) {
        return this.get<MemberA>(`/main/groups/${group}/members/${member}`);
    }

    patchMainGroupsPgroupMembersPmember(group: string, member: string, body: UpdateMemberQ) {
        return this.patch(`/main/groups/${group}/members/${member}`, body);
    }

    deleteMainGroupsPgroupMembersPmember(group: string, member: string) {
        return this.delete(`/main/groups/${group}/members/${member}`);
    }

    // --------------------
    // Main/Groups/Projects
    // --------------------

    getMainGroupsPgroupProjects(group: string) {
        return this.get<Array<ProjectA>>(`/main/groups/${group}/projects`);
    }

    // -------------
    // Main/Projects
    // -------------

    getMainProjects() {
        return this.get<Array<ProjectA>>('/main/projects');
    }

    postMainProjects(body: CreateProjectQ) {
        return this.post('/main/projects', body);
    }

    getMainProjectsPgroupPproject(group: string, project: string) {
        return this.get<ProjectA>(`/main/projects/${group}/${project}`);
    }

    patchMainProjectsPgroupPproject(
        group: string,
        project: string,
        body: UpdateProjectQ,
    ) {
        return this.patch(`/main/projects/${group}/${project}`, body);
    }

    deleteMainProjectsPgroupProject(group: string, project: string) {
        return this.delete(`/main/projects/${group}/${project}`);
    }

    // ---------------------
    // Main/Projects/Members
    // ---------------------

    getMainProjectsPgroupPprojectMembers(group: string, project: string) {
        return this.get<Array<MemberA>>(`/main/projects/${group}/${project}/members`);
    }

    postMainProjectsPgroupPprojectMembers(group: string, project: string, body: CreateMemberQ) {
        return this.post(`/main/projects/${group}/${project}/members`, body);
    }

    getMainProjectsPgroupPprojectMembersPmember(group: string, project: string, member: string) {
        return this.get<MemberA>(`/main/projects/${group}/${project}/members/${member}`);
    }

    patchMainProjectsPgroupPprojectMembersPmember(group: string, project: string, member: string, body: UpdateMemberQ) {
        return this.patch(`/main/projects/${group}/${project}/members/${member}`, body);
    }

    deleteMainProjectsPgroupPprojectMembersPmember(group: string, project: string, member: string) {
        return this.delete(`/main/projects/${group}/${project}/members/${member}`);
    }

    // ----------------
    // Main/Permissions
    // ----------------

    getMainPermissions() {
        return this.get<Array<PermissionA>>('/main/permissions');
    }

    getMainPermissionsPgroup(group: string) {
        return this.get<PermissionA>(`/main/permissions/${group}`);
    }

    getMainPermissionsPgroupPproject(group: string, project: string) {
        return this.get<PermissionA>(`/main/permissions/${group}/${project}`);
    }

    // ----------
    // Main/Infos
    // ----------

    getMainInfosOem() {
        return this.get<InfoA>(`/main/infos/oem`);
    }

    // --------------
    // Main/Usernames
    // --------------

    getMainUsernames() {
        return this.get<Array<string>>('/main/usernames');
    }

    // -------------
    // Admin/Configs
    // -------------

    getAdminConfigs() {
        return this.get<Array<ConfigA>>('/admin/configs');
    }

    getAdminConfigsPkey(key: string) {
        return this.get<ConfigA>(`/admin/configs/${key}`);
    }

    patchAdminConfigsPkey(key: string, body: UpdateConfigValueQ) {
        return this.patch(`/admin/configs/${key}`, body);
    }

    // -----------
    // Admin/Infos
    // -----------

    getAdminInfos() {
        return this.get<Array<InfoA>>('/admin/infos');
    }

    postAdminInfos(body: CreateInfoQ) {
        return this.post('/admin/infos', body);
    }

    getAdminInfosPkey(key: string) {
        return this.get<InfoA>(`/admin/infos/${key}`);
    }

    patchAdminInfosPkey(key: string, body: UpdateInfoQ) {
        return this.patch(`/admin/infos/${key}`, body);
    }

    deleteAdminInfo(key: string) {
        return this.delete(`/admin/infos/${key}`);
    }

    // ------------
    // Admin/System
    // ------------

    getAdminSystemOverview() {
        return this.get<SystemOverviewA>('/admin/system/overview');
    }

    // ---------------
    // Admin/Templates
    // ---------------

    getAdminTemplates() {
        return this.get<Array<TemplateA>>(`/admin/templates`);
    }

    // -----------
    // Admin/Users
    // -----------

    getAdminUsers() {
        return this.get<Array<UserA>>('/admin/users');
    }

    postAdminUsers(body: SignupQ) {
        return this.post('/admin/users', body);
    }

    getAdminUsersPuser(user: string) {
        return this.get<UserA>(`/admin/users/${user}`);
    }

    patchAdminUsersPuser(user: string, body: UpdateUserQ) {
        return this.patch(`/admin/users/${user}`, body);
    }

    deleteAdminUsersPuser(user: string) {
        return this.delete(`/admin/users/${user}`);
    }

    // ------------
    // Admin/Groups
    // ------------

    getAdminGroups() {
        return this.get<Array<GroupA>>('/admin/groups');
    }

    postAdminGroups(body: CreateGroupQ) {
        return this.post('/admin/groups', body);
    }

    getAdminGroupsPgroup(group: string) {
        return this.get<GroupA>(`/admin/groups/${group}`);
    }

    patchAdminGroupsPgroup(group: string, body: UpdateGroupQ) {
        return this.patch(`/admin/groups/${group}`, body);
    }

    deleteAdminGroupsGroup(group: string) {
        return this.delete(`/admin/groups/${group}`);
    }

    // --------------
    // Admin/Projects
    // --------------

    getAdminProjects() {
        return this.get<Array<ProjectA>>('/admin/projects');
    }

    postAdminProjects(body: CreateProjectQ) {
        return this.post('/admin/projects', body);
    }

    getAdminProjectsPgroupPproject(group: string, project: string) {
        return this.get<ProjectA>(`/admin/projects/${group}/${project}`);
    }

    patchAdminProjectsPgroupPproject(group: string, project: string, body: UpdateProjectQ) {
        return this.patch(`/admin/projects/${group}/${project}`, body);
    }

    deleteAdminProjectsPgroupProject(group: string, project: string) {
        return this.delete(`/admin/projects/${group}/${project}`);
    }

    // -----------------
    // Admin/Permissions
    // -----------------

    getAdminPermissions() {
        return this.get<Array<PermissionA>>('/admin/permissions');
    }

    postAdminPermissions(body: CreatePermissionQ) {
        return this.post('/admin/permissions', body);
    }

    getAdminPermissionsPperm(perm: string) {
        return this.get<PermissionA>(`/admin/permissions/${perm}`);
    }

    patchAdminPermissionsPperm(perm: string, body: UpdatePermissionQ) {
        return this.patch(`/admin/permissions/${perm}`, body);
    }

    deleteAdminPermissionsPperm(perm: string) {
        return this.delete(`/admin/permissions/${perm}`);
    }

    // --------------
    // Plugins/Airjoy
    // --------------

    getAirjoyLive(group: string, project: string) {
        return this.get<Array<AirjoySensorA>>(`/plugins/airjoy/${group}/${project}/live`);
    }
}
