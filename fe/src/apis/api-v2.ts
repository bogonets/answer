import AxiosLib from 'axios';
import type {
    AxiosInstance,
    AxiosResponse,
    AxiosRequestConfig,
    AxiosBasicCredentials,
} from 'axios';
import type {
    AirjoySensorA,
    AirjoyDeviceA,
    CreateAirjoyDeviceQ,
    UpdateAirjoyDeviceQ,
    AirjoyControlQ,
    AirjoyChartA,
    AirjoyChartQ,
    AirjoyServiceA,
    CreateAirjoyServiceQ,
    UpdateAirjoyServiceQ,
} from '@/packet/airjoy';
import type {
    VmsDeviceA,
    VmsCreateDeviceQ,
    VmsUpdateDeviceQ,
    VmsLayoutA,
    VmsCreateLayoutQ,
    VmsUpdateLayoutQ,
    VmsEventConfigA,
    VmsCreateEventConfigQ,
    VmsUpdateEventConfigQ,
    VmsEventTagA,
    VmsCreateEventTagQ,
    VmsUpdateEventTagQ,
    VmsEventA,
    VmsNewsEventQ,
    VmsDiscoveryQ,
    VmsDiscoveredHeartbeatQ,
    VmsDiscoveredHeartbeatA,
    VmsOnvifMediaStreamUriQ,
    VmsOnvifMediaStreamUriHeartbeatQ,
    VmsOnvifMediaStreamUriHeartbeatA,
    VmsOnvifMediaSnapshotQ,
    VmsOnvifMediaSnapshotA,
    IceServerA,
    RtcOfferQ,
    RtcAnswerA,
} from '@/packet/vms';
import type {ConfigA, UpdateConfigValueQ} from '@/packet/config';
import type {ContainerA, ControlContainersQ} from '@/packet/container';
import type {GroupA, CreateGroupQ, UpdateGroupQ} from '@/packet/group';
import type {InfoA, CreateInfoQ, UpdateInfoQ} from '@/packet/info';
import type {
    RawPermission,
    PermissionA,
    CreatePermissionQ,
    UpdatePermissionQ,
} from '@/packet/permission';
import type {PluginA, PluginNameA} from '@/packet/plugin';
import type {DaemonA, CreateDaemonQ, UpdateDaemonQ} from '@/packet/daemon';
import type {TemplateA} from '@/packet/template';
import type {
    ProjectA,
    CreateProjectQ,
    UpdateProjectQ,
    ProjectOverviewA,
} from '@/packet/project';
import type {MemberA, CreateMemberQ, UpdateMemberQ} from '@/packet/member';
import type {SystemOverviewA, VersionsA} from '@/packet/system';
import type {
    UserA,
    UpdateUserQ,
    SigninA,
    SignupQ,
    UpdatePasswordQ,
    UserExtraA,
    RefreshTokenA,
} from '@/packet/user';
import type {EnvironmentA} from '@/packet/environment';
import {createEmptySigninA, createEmptyUserA} from '@/packet/user';
import {PreferenceA, createEmptyPreference} from '@/packet/preference';
import {encryptSha256} from '@/crypto/sha';
import moment from 'moment-timezone';

const DEFAULT_TIMEOUT = 30 * 1000;
const STATUS_CODE_ACCESS_TOKEN_ERROR = 461
const STATUS_CODE_REFRESH_TOKEN_ERROR = 462
const STATUS_CODE_UNINITIALIZED_SERVICE = 561

const LEEWAY_MILLISECONDS = DEFAULT_TIMEOUT;

const VALIDATE_STATUS = [
    200,
    STATUS_CODE_ACCESS_TOKEN_ERROR,
    STATUS_CODE_REFRESH_TOKEN_ERROR,
    STATUS_CODE_UNINITIALIZED_SERVICE,
];

const HEADER_KEY_AUTHORIZATION = 'Authorization';

export class UninitializedServiceError extends Error {
    constructor() {
        super('Uninitialized service');
    }
}

export class TokenError extends Error {
    constructor(message?: string) {
        super(message);
    }
}

export class AccessTokenError extends TokenError {
    constructor(message = 'Access Token Error') {
        super(message);
    }
}

export class RefreshTokenError extends TokenError {
    constructor(message = 'Refresh Token Error') {
        super(message);
    }
}

export function originToBaseUrl(origin: string): string {
    if (origin[origin.length-1] == '/') {
        return origin + 'api/v2';
    } else {
        return origin + '/api/v2';
    }
}

export interface ApiV2Options {
    origin?: string;
    timeout?: number;

    accessTokenErrorCallback?: () => void;
    refreshTokenErrorCallback?: () => void;
    uninitializedServiceCallback?: () => void;
    renewalAccessTokenCallback?: (access: string) => void;
}

export default class ApiV2 {

    readonly accessTokenErrorCallback?: () => void;
    readonly refreshTokenErrorCallback?: () => void;
    readonly uninitializedServiceCallback?: () => void;
    readonly renewalAccessTokenCallback?: (access: string) => void;

    originAddress: string;
    api: AxiosInstance;
    session: SigninA;

    refreshTimeoutId?: number = undefined;

    constructor(options?: ApiV2Options) {
        this.accessTokenErrorCallback = options?.accessTokenErrorCallback;
        this.refreshTokenErrorCallback = options?.refreshTokenErrorCallback;
        this.uninitializedServiceCallback = options?.uninitializedServiceCallback;
        this.renewalAccessTokenCallback = options?.renewalAccessTokenCallback;

        const origin = options?.origin || document.location.origin;
        const timeout = options?.timeout || DEFAULT_TIMEOUT;

        this.originAddress = origin;
        this.api = AxiosLib.create({
            baseURL: originToBaseUrl(origin),
            timeout: timeout,
            headers: {
                Accept: 'application/json',
            },
            validateStatus: (status: number): boolean => {
                return VALIDATE_STATUS.includes(status);
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

    refreshToken(refresh: string) {
        console.debug('Refreshing access token ...');
        this.refreshTimeoutId = undefined;

        const config = {
            headers: {
                'Authorization': `Bearer ${refresh}`,
            },
        } as AxiosRequestConfig;

        return this.api.post('/public/token/refresh', undefined, config)
            .then((response: AxiosResponse) => {
                const result = response.data as RefreshTokenA;
                if (this.renewalAccessTokenCallback) {
                    this.renewalAccessTokenCallback(result.access);
                }
                this.setDefaultAccessToken(result.access, refresh);
                console.info('Access token renewal successful');
            })
            .catch(error => {
                console.error(error);
            });
    }

    private cancelTokenRenewal() {
        if (typeof this.refreshTimeoutId === 'undefined') {
            return;
        }

        window.clearTimeout(this.refreshTimeoutId);
        this.refreshTimeoutId = undefined;
        console.debug(`Token renewal canceled`);
    }

    private reservationTokenRenewal(access: string, refresh: string) {
        const encodedPayload = access.split('.')[1];
        const payloadJsonText = atob(encodedPayload)
        const parsed = JSON.parse(payloadJsonText.toString());
        const hasExp = parsed.hasOwnProperty("exp");
        const hasIat = parsed.hasOwnProperty("iat");

        if (!hasExp || !hasIat) {
            if (!hasExp) {
                console.error('Missing `exp` in JWT payload');
            }
            if (!hasIat) {
                console.error('Missing `iat` in JWT payload');
            }
            return;
        }

        // const nowUtc = moment();
        // const expUtc = moment(parsed.exp * 1000);
        // const iatUtc = moment(parsed.iat * 1000);
        // console.debug('Access token expiration: ' + expUtc.toISOString());

        const expMilliseconds = (parsed.exp * 1000 - LEEWAY_MILLISECONDS);
        const timeout = expMilliseconds - Date.now();
        if (typeof this.refreshTimeoutId !== 'undefined') {
            window.clearTimeout(this.refreshTimeoutId);
            this.refreshTimeoutId = undefined;
        }

        if (timeout >= 0) {
            this.refreshTimeoutId = window.setTimeout(() => {
                this.refreshToken(refresh).finally();
            }, timeout);
        } else {
            this.refreshToken(refresh).finally();
        }

        const renewalTime = moment(Date.now() + timeout).toISOString();
        console.debug(`Token renewal timeout: ${timeout}ms (${renewalTime})`);
    }

    clearDefaultSession() {
        this.session.access = '';
        this.session.refresh = '';
        this.session.user = createEmptyUserA();
        this.session.preference = createEmptyPreference();
        if (this.api.defaults.headers.hasOwnProperty(HEADER_KEY_AUTHORIZATION)) {
            delete this.api.defaults.headers[HEADER_KEY_AUTHORIZATION];
        }
        this.cancelTokenRenewal();
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
        this.api.defaults.headers[HEADER_KEY_AUTHORIZATION] = `Bearer ${access}`;
        this.reservationTokenRenewal(access, refresh);
    }

    setDefaultAccessToken(access: string, refresh: string) {
        this.session.access = access;
        this.api.defaults.headers[HEADER_KEY_AUTHORIZATION] = `Bearer ${access}`;
        this.reservationTokenRenewal(access, refresh);
    }

    private commonErrorHandling<T>(res: AxiosResponse<T>) {
        if (res.status === STATUS_CODE_ACCESS_TOKEN_ERROR) {
            if (this.accessTokenErrorCallback) {
                this.accessTokenErrorCallback();
            }
            this.clearDefaultSession();
            throw new AccessTokenError();
        } else if (res.status === STATUS_CODE_REFRESH_TOKEN_ERROR) {
            if (this.refreshTokenErrorCallback) {
                this.refreshTokenErrorCallback();
            }
            this.clearDefaultSession();
            throw new RefreshTokenError();
        } else if (res.status === STATUS_CODE_UNINITIALIZED_SERVICE) {
            if (this.uninitializedServiceCallback) {
                this.uninitializedServiceCallback();
            }
            throw new UninitializedServiceError();
        }
        console.assert(res.status === 200);
    }

    get<T = any>(url: string, config?: AxiosRequestConfig) {
        return this.api.get<T>(url, config).then(res => {
            this.commonErrorHandling(res);
            return res.data;
        });
    }

    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
        return this.api.post<T>(url, data, config).then(res => {
            this.commonErrorHandling(res);
            return res.data;
        });
    }

    patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
        return this.api.patch<T>(url, data, config).then(res => {
            this.commonErrorHandling(res);
            return res.data;
        });
    }

    delete(url: string, config?: AxiosRequestConfig) {
        return this.api.delete(url, config).then(res => {
            this.commonErrorHandling(res);
        });
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
                    throw new AccessTokenError('Empty access token error');
                }
                if (!refresh) {
                    throw new RefreshTokenError('Empty refresh token error');
                }
                if (updateDefaultAuth) {
                    const user = result.user || createEmptyUserA();
                    const preference = result.preference || createEmptyPreference();
                    this.setDefaultSession(access, refresh, user, preference);
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

    deleteSelf() {
        return this.delete('/self');
    }

    getSelfExtra() {
        return this.get<UserExtraA>('/self/extra');
    }

    patchSelfExtra(extra: UserExtraA) {
        return this.patch('/self/extra', extra);
    }

    patchSelfPassword(body: UpdatePasswordQ) {
        return this.patch('/self/password', body);
    }

    getSelfRawPermissionPgroup(group: string) {
        return this.get<RawPermission>(`/self/raw/permission/${group}`);
    }

    getSelfRawPermissionPgroupPproject(group: string, project: string) {
        return this.get<RawPermission>(`/self/raw/permission/${group}/${project}`);
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

    // ----------------------
    // Main/Projects/Overview
    // ----------------------

    getMainProjectsPgroupPprojectOverview(group: string, project: string) {
        const url = `/main/projects/${group}/${project}/overview`;
        return this.get<ProjectOverviewA>(url);
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

    // ------------
    // Admin/System
    // ------------

    getAdminSystemOverview() {
        return this.get<SystemOverviewA>('/admin/system/overview');
    }

    // ------------
    // Admin/Plugin
    // ------------

    getAdminPluginNames() {
        return this.get<Array<PluginNameA>>('/admin/plugin/names');
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

    // ----------------
    // Admin/Containers
    // ----------------

    getAdminContainers() {
        return this.get<Array<ContainerA>>('/admin/containers');
    }

    patchAdminContainers(body: ControlContainersQ) {
        return this.patch('/admin/containers', body);
    }

    // -----------
    // Dev/Configs
    // -----------

    getDevConfigs() {
        return this.get<Array<ConfigA>>('/dev/configs');
    }

    getDevConfigsPkey(key: string) {
        return this.get<ConfigA>(`/dev/configs/${key}`);
    }

    patchDevConfigsPkey(key: string, body: UpdateConfigValueQ) {
        return this.patch(`/dev/configs/${key}`, body);
    }

    // ---------
    // Dev/Infos
    // ---------

    getDevInfos() {
        return this.get<Array<InfoA>>('/dev/infos');
    }

    postDevInfos(body: CreateInfoQ) {
        return this.post('/dev/infos', body);
    }

    getDevInfosPkey(key: string) {
        return this.get<InfoA>(`/dev/infos/${key}`);
    }

    patchDevInfosPkey(key: string, body: UpdateInfoQ) {
        return this.patch(`/dev/infos/${key}`, body);
    }

    deleteDevInfo(key: string) {
        return this.delete(`/dev/infos/${key}`);
    }

    // ----------
    // Dev/System
    // ----------

    getDevSystemVersions() {
        return this.get<VersionsA>('/dev/system/versions');
    }

    // -----------
    // Dev/Plugins
    // -----------

    getDevPlugins() {
        return this.get<Array<PluginA>>('/dev/plugins');
    }

    // ----------------
    // Dev/Environments
    // ----------------

    getDevEnvironments() {
        return this.get<Array<EnvironmentA>>('/dev/environments');
    }

    // ----------
    // Dev/Daemon
    // ----------

    getDevDaemonPlugins() {
        return this.get<Array<string>>('/dev/daemon/plugins');
    }

    getDevDaemons() {
        return this.get<Array<DaemonA>>('/dev/daemons');
    }

    postDevDaemons(body: CreateDaemonQ) {
        return this.post('/dev/daemons', body);
    }

    getDevDaemonsPdaemon(daemon: string) {
        return this.get<DaemonA>(`/dev/daemons/${daemon}`);
    }

    patchDevDaemonsPdaemon(daemon: string, body: UpdateDaemonQ) {
        return this.patch(`/dev/daemons/${daemon}`, body);
    }

    deleteDevDaemonsPdaemon(daemon: string) {
        return this.delete(`/dev/daemons/${daemon}`);
    }

    postDevDaemonsPdaemonStart(daemon: string) {
        return this.post(`/dev/daemons/${daemon}/start`);
    }

    postDevDaemonsPdaemonStop(daemon: string) {
        return this.post(`/dev/daemons/${daemon}/stop`);
    }

    // --------------
    // Plugins/Airjoy
    // --------------

    getAirjoyLive(group: string, project: string) {
        const url = `/plugins/airjoy/${group}/${project}/live`;
        return this.get<Array<AirjoySensorA>>(url);
    }

    getAirjoyDevices(group: string, project: string) {
        const url = `/plugins/airjoy/${group}/${project}/devices`;
        return this.get<Array<AirjoyDeviceA>>(url);
    }

    postAirjoyDevices(group: string, project: string, body: CreateAirjoyDeviceQ) {
        const url = `/plugins/airjoy/${group}/${project}/devices`;
        return this.post(url, body);
    }

    getAirjoyDevice(
        group: string,
        project: string,
        device: number | string,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
        return this.get<AirjoyDeviceA>(url);
    }

    patchAirjoyDevice(
        group: string,
        project: string,
        device: number | string,
        body: UpdateAirjoyDeviceQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
        return this.patch(url, body);
    }

    deleteAirjoyDevice(
        group: string,
        project: string,
        device: number | string,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
        return this.delete(url);
    }

    postAirjoyControl(
        group: string,
        project: string,
        device: number | string,
        body: AirjoyControlQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/control`;
        return this.post(url, body);
    }

    getAirjoyChart(
        group: string,
        project: string,
        device: number | string,
        begin: string,
        end: string,
        category: string,
        period?: string,
        origin?: string,
    ) {
        const body = {
            begin: begin,
            end: end,
            category: category,
            period: period,
            origin: origin,
        } as AirjoyChartQ;
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/chart`;
        return this.post<Array<AirjoyChartA>>(url, body);  // TODO: Change to 'GET' method
    }

    getAirjoyServices(
        group: string,
        project: string,
        device?: number | string,
    ) {
        if (typeof device === 'undefined') {
            const url = `/plugins/airjoy/${group}/${project}/services`;
            return this.get<Array<AirjoyServiceA>>(url);
        } else {
            const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services`;
            return this.get<Array<AirjoyServiceA>>(url);
        }
    }

    postAirjoyServices(
        group: string,
        project: string,
        device: number | string,
        body: CreateAirjoyServiceQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services`;
        return this.post(url, body);
    }

    patchAirjoyServices(
        group: string,
        project: string,
        device: number | string,
        service: number | string,
        body: UpdateAirjoyServiceQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services/${service}`;
        return this.patch(url, body);
    }

    deleteAirjoyServices(
        group: string,
        project: string,
        device: number | string,
        service: number | string,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services/${service}`;
        return this.delete(url);
    }

    // -------------------
    // Plugins/VMS/Devices
    // -------------------

    getVmsDevices(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/devices`;
        return this.get<Array<VmsDeviceA>>(url);
    }

    postVmsDevices(group: string, project: string, body: VmsCreateDeviceQ) {
        const url = `/plugins/vms/${group}/${project}/devices`;
        return this.post(url, body);
    }

    getVmsDevice(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}`;
        return this.get<VmsDeviceA>(url);
    }

    patchVmsDevice(
        group: string,
        project: string,
        device: string,
        body: VmsUpdateDeviceQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}`;
        return this.patch(url, body);
    }

    deleteVmsDevice(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}`;
        return this.delete(url);
    }

    postVmsDeviceProcessStart(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/process/start`;
        return this.post(url);
    }

    postVmsDeviceProcessStop(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/process/stop`;
        return this.post(url);
    }

    getVmsDeviceRtcIces(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/rtc/ices`;
        return this.get<Array<IceServerA>>(url);
    }

    postVmsDeviceRtcJsep(
        group: string,
        project: string,
        device: string,
        body: RtcOfferQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/rtc/jsep`;
        return this.post<RtcAnswerA>(url, body);
    }

    // -------------------
    // Plugins/VMS/Layouts
    // -------------------

    getVmsLayouts(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/layouts`;
        return this.get<Array<VmsLayoutA>>(url);
    }

    postVmsLayouts(group: string, project: string, body: VmsCreateLayoutQ) {
        const url = `/plugins/vms/${group}/${project}/layouts`;
        return this.post(url, body);
    }

    getVmsLayout(group: string, project: string, layout: string) {
        const url = `/plugins/vms/${group}/${project}/layouts/${layout}`;
        return this.get<VmsLayoutA>(url);
    }

    patchVmsLayout(
        group: string,
        project: string,
        layout: string,
        body: VmsUpdateLayoutQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/layouts/${layout}`;
        return this.patch(url, body);
    }

    deleteVmsLayout(group: string, project: string, layout: string) {
        const url = `/plugins/vms/${group}/${project}/layouts/${layout}`;
        return this.delete(url);
    }

    // -----------------
    // Plugins/VMS/Event
    // -----------------

    postVmsEventsNews(group: string, project: string, body: VmsNewsEventQ) {
        const url = `/plugins/vms/${group}/${project}/events/news`;
        return this.post<Array<VmsEventA>>(url, body);
    }

    getVmsEventsConfigs(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/events/configs`;
        return this.get<Array<VmsEventConfigA>>(url);
    }

    postVmsEventsConfigs(group: string, project: string, body: VmsCreateEventConfigQ) {
        const url = `/plugins/vms/${group}/${project}/events/configs`;
        return this.post(url, body);
    }

    getVmsEventsConfigsPconfig(group: string, project: string, config: string) {
        const url = `/plugins/vms/${group}/${project}/events/configs/${config}`;
        return this.get<VmsEventConfigA>(url);
    }

    patchVmsEventsConfigsPconfig(
        group: string,
        project: string,
        config: string,
        body: VmsUpdateEventConfigQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/events/configs/${config}`;
        return this.patch(url, body);
    }

    deleteVmsEventsConfigsPconfig(group: string, project: string, config: string) {
        const url = `/plugins/vms/${group}/${project}/events/configs/${config}`;
        return this.delete(url);
    }

    getVmsEventsTags(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/events/tags`;
        return this.get<Array<VmsEventTagA>>(url);
    }

    postVmsEventsTags(group: string, project: string, body: VmsCreateEventTagQ) {
        const url = `/plugins/vms/${group}/${project}/events/tags`;
        return this.post(url, body);
    }

    getVmsEventsTagsPtag(group: string, project: string, tag: string) {
        const url = `/plugins/vms/${group}/${project}/events/tags/${tag}`;
        return this.get<VmsEventTagA>(url);
    }

    patchVmsEventsTagsPtag(
        group: string,
        project: string,
        tag: string,
        body: VmsUpdateEventTagQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/events/tags/${tag}`;
        return this.patch(url, body);
    }

    deleteVmsEventsTagsPtag(group: string, project: string, tag: string) {
        const url = `/plugins/vms/${group}/${project}/events/tags/${tag}`;
        return this.delete(url);
    }

    // ---------------------
    // Plugins/VMS/Discovery
    // ---------------------

    postVmsDiscovery(
        group: string,
        project: string,
        body: VmsDiscoveryQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/discovery`;
        return this.post(url, body);
    }

    postVmsDiscoveryHeartbeat(
        group: string,
        project: string,
        body: VmsDiscoveredHeartbeatQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/discovery/heartbeat`;
        return this.post<VmsDiscoveredHeartbeatA>(url, body);
    }

    // -----------------------
    // Plugins/VMS/ONVIF/Media
    // -----------------------

    postVmsOnvifMedia(
        group: string,
        project: string,
        body: VmsOnvifMediaStreamUriQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/onvif/media`;
        return this.post(url, body);
    }

    postVmsOnvifMediaHeartbeat(
        group: string,
        project: string,
        body: VmsOnvifMediaStreamUriHeartbeatQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/onvif/media/heartbeat`;
        return this.post<VmsOnvifMediaStreamUriHeartbeatA>(url, body);
    }

    postVmsOnvifMediaSnapshot(
        group: string,
        project: string,
        body: VmsOnvifMediaSnapshotQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/onvif/media/snapshot`;
        return this.post<VmsOnvifMediaSnapshotA>(url, body);
    }
}
