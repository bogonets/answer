import Vue from 'vue';

import {Store} from 'vuex';
import {LocalStore} from '@/store/LocalStore';

import router from '@/router';
import rootNames from '@/router/names/root';
import {RawLocation} from 'vue-router';

import {encryptSha256} from '@/crypto/sha';

import AxiosLib, {AxiosError} from 'axios';
import type {
    AxiosInstance,
    AxiosResponse,
    AxiosRequestConfig,
    AxiosBasicCredentials,
} from 'axios';

import type {
    AirjoySensorA,
    AirjoyDeviceA,
    AirjoyCreateDeviceQ,
    AirjoyUpdateDeviceQ,
    AirjoyControlQ,
    AirjoyChartA,
    AirjoyServiceA,
    AirjoyCreateServiceQ,
    AirjoyUpdateServiceQ,
} from '@/packet/airjoy';
import type {
    VmsImageA,
    VmsUploadImageQ,
    VmsUploadImageA,
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
    VmsFilterEventQ,
    VmsNewsEventQ,
    VmsLatestEventQ,
    VmsEventImageA,
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
    VmsEventConfigColorQ,
    VmsEventConfigDetectionQ,
    VmsEventConfigMatchingQ,
    VmsEventConfigOcrQ,
} from '@/packet/vms';

import type {ConfigA, UpdateConfigValueQ} from '@/packet/config';
import type {ContainerA, ControlContainersQ} from '@/packet/container';
import type {GroupA, CreateGroupQ, UpdateGroupQ} from '@/packet/group';
import type {InfoA, CreateInfoQ, UpdateInfoQ} from '@/packet/info';
import type {PluginA, PluginNameA} from '@/packet/plugin';
import type {TemplateA} from '@/packet/template';
import type {DaemonA, CreateDaemonQ, UpdateDaemonQ} from '@/packet/daemon';
import type {MemberA, CreateMemberQ, UpdateMemberQ} from '@/packet/member';
import type {SystemOverviewA, VersionsA} from '@/packet/system';
import type {RoleA, CreateRoleQ, UpdateRoleQ} from '@/packet/role';
import type {
    ProjectA,
    CreateProjectQ,
    UpdateProjectQ,
    ProjectOverviewA,
} from '@/packet/project';
import type {
    UserA,
    UpdateUserQ,
    SigninA,
    SignupQ,
    UpdatePasswordQ,
    UserExtraA,
    RefreshTokenA,
} from '@/packet/user';
import {
    createEmptySigninA,
    createEmptyUserA
} from '@/packet/user';
import type {EnvironmentA} from '@/packet/environment';
import type {PreferenceA} from '@/packet/preference';
import {createEmptyPreference} from '@/packet/preference';
import type {VmsRecordRangeA} from '@/packet/vms/record_range';
import type {PortA, PortRangeA} from '@/packet/port';

const DEFAULT_TIMEOUT_MILLISECONDS = 30 * 1000;
const STATUS_CODE_ACCESS_TOKEN_ERROR = 461
const STATUS_CODE_REFRESH_TOKEN_ERROR = 462
const STATUS_CODE_UNINITIALIZED_SERVICE = 561
const VALIDATE_STATUS = [200];
const HEADER_AUTHORIZATION = 'Authorization';

function originToBaseUrl(origin: string): string {
    if (origin[origin.length-1] == '/') {
        return origin + 'api/v2';
    } else {
        return origin + '/api/v2';
    }
}

function moveTo(name: string) {
    if (router.currentRoute.name === name) {
        return;
    }

    const rawLocation = {
        name: name,
    } as RawLocation;

    router.push(rawLocation).catch((reason: any) => {
        if (reason.name !== 'NavigationDuplicated') {
            throw reason;
        }
    });
}

function clearSession() {
    const localStore = Vue.prototype.$localStore as LocalStore;
    localStore.clearSession();

    const sessionStore = Vue.prototype.$store as Store<any>;
    sessionStore.commit('user/logout');
}

function renewalAccessToken(access: string) {
    const localStore = Vue.prototype.$localStore as LocalStore;
    localStore.access = access;

    const sessionStore = Vue.prototype.$store as Store<any>;
    sessionStore.commit('user/renewalAccessToken', {
        accessToken: access,
    });
}

export interface ApiV2Options {
    origin?: string;
    timeout?: number;
}

export default class ApiV2 {

    originAddress: string;
    session: SigninA;
    api: AxiosInstance;

    refreshing = false;
    refreshSubscribers = [] as Array<(string) => any>;

    constructor(options?: ApiV2Options) {
        const origin = options?.origin || document.location.origin;
        const timeout = options?.timeout || DEFAULT_TIMEOUT_MILLISECONDS;

        this.originAddress = origin;
        this.session = createEmptySigninA();
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
        this.api.interceptors.response.use(
            (response) => {
                return response;
            },
            (error) => {
                return this.onResponseRejected(error);
            },
        );
    }

    get baseURL() {
        return this.api.defaults.baseURL;
    }

    get origin() {
        return this.originAddress;
    }

    set origin(origin: string) {
        this.originAddress = origin;
        this.api.defaults.baseURL = originToBaseUrl(origin);
    }

    async onResponseRejected(error: AxiosError) {
        if (!error.response) {
            return Promise.reject(new Error('Undefined response object'));
        }

        const status = error.response.status;
        if (status === STATUS_CODE_REFRESH_TOKEN_ERROR) {
            clearSession();
            moveTo(rootNames.signin);
            return Promise.reject(new Error('Expired refresh token'));
        }

        if (status === STATUS_CODE_UNINITIALIZED_SERVICE) {
            clearSession();
            moveTo(rootNames.init);
            return Promise.reject('Uninitialized service');
        }

        if (status === STATUS_CODE_ACCESS_TOKEN_ERROR) {
            const originalConfig = error.config;

            if (this.refreshing) {
                return new Promise((resolve, reject) => {
                    this.refreshSubscribers.push((access?: string) => {
                        if (access) {
                            originalConfig.headers.Authorization = `Bearer ${access}`;
                            resolve(this.api(originalConfig));
                        } else {
                            reject(new Error('Refresh token error'));
                        }
                    });
                });
            } else {
                this.refreshing = true;

                try {
                    const refreshTokenConfig = {
                        headers: {'Authorization': `Bearer ${this.session.refresh}`},
                    } as AxiosRequestConfig;

                    console.debug('Refreshing access token ...');
                    const refreshTokenResult = await this.api.post<RefreshTokenA>(
                        '/public/token/refresh', undefined, refreshTokenConfig
                    );
                    const access = refreshTokenResult.data.access;

                    originalConfig.headers[HEADER_AUTHORIZATION] = `Bearer ${access}`;
                    renewalAccessToken(access);
                    this.setDefaultAccessToken(access);
                    console.info('Access token renewal successful');

                    this.refreshing = false;
                    const subscribers = this.refreshSubscribers;
                    this.refreshSubscribers = [];
                    subscribers.map(cb => cb(access));

                    // Retry the failed request.
                    return this.api(originalConfig);
                } catch (error) {
                    console.error(`Refresh token error: ${error}`);

                    this.refreshing = false;
                    const subscribers = this.refreshSubscribers;
                    this.refreshSubscribers = [];
                    subscribers.map(cb => cb(undefined));

                    clearSession();
                    moveTo(rootNames.signin);
                    return Promise.reject(error);
                }
            }
        }

        return Promise.reject(error);
    }

    // private reservationTokenRenewal(access: string, refresh: string) {
    //     const encodedPayload = access.split('.')[1];
    //     const payloadJsonText = atob(encodedPayload)
    //     const parsed = JSON.parse(payloadJsonText.toString());
    //     const hasExp = parsed.hasOwnProperty("exp");
    //     const hasIat = parsed.hasOwnProperty("iat");
    //
    //     if (!hasExp || !hasIat) {
    //         if (!hasExp) {
    //             console.error('Missing `exp` in JWT payload');
    //         }
    //         if (!hasIat) {
    //             console.error('Missing `iat` in JWT payload');
    //         }
    //         return;
    //     }
    //
    //     // const nowUtc = moment();
    //     // const expUtc = moment(parsed.exp * 1000);
    //     // const iatUtc = moment(parsed.iat * 1000);
    //     // console.debug('Access token expiration: ' + expUtc.toISOString());
    //
    //     const expMilliseconds = (parsed.exp * 1000 - LEEWAY_MILLISECONDS);
    //     const timeout = expMilliseconds - Date.now();
    //     if (typeof this.refreshTimeoutId !== 'undefined') {
    //         window.clearTimeout(this.refreshTimeoutId);
    //         this.refreshTimeoutId = undefined;
    //     }
    //
    //     if (timeout >= 0) {
    //         this.refreshTimeoutId = window.setTimeout(() => {
    //             this.refreshToken(refresh).finally();
    //         }, timeout);
    //     } else {
    //         this.refreshToken(refresh).finally();
    //     }
    //
    //     const renewalTime = moment(Date.now() + timeout).toISOString();
    //     console.debug(`Token renewal timeout: ${timeout}ms (${renewalTime})`);
    // }

    clearDefaultSession() {
        this.session.access = '';
        this.session.refresh = '';
        this.session.user = createEmptyUserA();
        this.session.preference = createEmptyPreference();
        if (this.api.defaults.headers.hasOwnProperty(HEADER_AUTHORIZATION)) {
            delete this.api.defaults.headers[HEADER_AUTHORIZATION];
        }
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
        this.api.defaults.headers[HEADER_AUTHORIZATION] = `Bearer ${access}`;
    }

    setDefaultAccessToken(access: string) {
        this.session.access = access;
        this.api.defaults.headers[HEADER_AUTHORIZATION] = `Bearer ${access}`;
    }

    get<T = any>(url: string, config?: AxiosRequestConfig) {
        return this.api.get<T>(url, config).then(res => {
            return res.data;
        });
    }

    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
        return this.api.post<T>(url, data, config).then(res => {
            return res.data;
        });
    }

    patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig) {
        return this.api.patch<T>(url, data, config).then(res => {
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

    getSelfPermissionsPgroup(group: string) {
        return this.get<Array<string>>(`/self/permissions/${group}`);
    }

    getSelfPermissionsPgroupPproject(group: string, project: string) {
        return this.get<Array<string>>(`/self/permissions/${group}/${project}`);
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
        return this.get<Array<string>>('/main/permissions');
    }

    // ----------
    // Main/Roles
    // ----------

    getMainRoles() {
        return this.get<Array<RoleA>>('/main/roles');
    }

    getMainRolesPgroup(group: string) {
        return this.get<RoleA>(`/main/roles/${group}`);
    }

    getMainRolesPgroupPproject(group: string, project: string) {
        return this.get<RoleA>(`/main/roles/${group}/${project}`);
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

    // -----------
    // Admin/Roles
    // -----------

    getAdminRoles() {
        return this.get<Array<RoleA>>('/admin/roles');
    }

    postAdminRoles(body: CreateRoleQ) {
        return this.post('/admin/roles', body);
    }

    getAdminRolesProle(role: string) {
        return this.get<RoleA>(`/admin/roles/${role}`);
    }

    patchAdminRolesProle(role: string, body: UpdateRoleQ) {
        return this.patch(`/admin/roles/${role}`, body);
    }

    deleteAdminRolesProle(role: string) {
        return this.delete(`/admin/roles/${role}`);
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

    // ------------
    // Admin/Daemon
    // ------------

    getAdminDaemonPlugins() {
        return this.get<Array<string>>('/admin/daemon/plugins');
    }

    getAdminDaemons() {
        return this.get<Array<DaemonA>>('/admin/daemons');
    }

    postAdminDaemons(body: CreateDaemonQ) {
        return this.post('/admin/daemons', body);
    }

    getAdminDaemonsPdaemon(daemon: string) {
        return this.get<DaemonA>(`/admin/daemons/${daemon}`);
    }

    patchAdminDaemonsPdaemon(daemon: string, body: UpdateDaemonQ) {
        return this.patch(`/admin/daemons/${daemon}`, body);
    }

    deleteAdminDaemonsPdaemon(daemon: string) {
        return this.delete(`/admin/daemons/${daemon}`);
    }

    postAdminDaemonsPdaemonStart(daemon: string) {
        return this.post(`/admin/daemons/${daemon}/start`);
    }

    postAdminDaemonsPdaemonStop(daemon: string) {
        return this.post(`/admin/daemons/${daemon}/stop`);
    }

    // -----------
    // Admin/Ports
    // -----------

    getAdminPorts() {
        return this.get<Array<PortA>>('/admin/ports');
    }

    getAdminPortsRange() {
        return this.get<PortRangeA>('/admin/ports?op=range');
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

    postAirjoyDevices(group: string, project: string, body: AirjoyCreateDeviceQ) {
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
        body: AirjoyUpdateDeviceQ,
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
    ) {
        const queryBegin = encodeURIComponent(begin);
        const queryEnd = encodeURIComponent(end);
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/chart`;
        const query = `?begin=${queryBegin}&end=${queryEnd}`;
        return this.get<Array<AirjoyChartA>>(url + query);
    }

    getAirjoyChartCsv(
        group: string,
        project: string,
        device: number | string,
        begin: string,
        end: string,
    ) {
        const queryBegin = encodeURIComponent(begin);
        const queryEnd = encodeURIComponent(end);
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/chart/csv`;
        const query = `?begin=${queryBegin}&end=${queryEnd}`;
        return this.get<string>(url + query);
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
        body: AirjoyCreateServiceQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services`;
        return this.post(url, body);
    }

    patchAirjoyServices(
        group: string,
        project: string,
        device: number | string,
        service: number | string,
        body: AirjoyUpdateServiceQ,
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

    deleteVmsDeviceRtcJsep(
        group: string,
        project: string,
        device: string,
        peer: string,
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/rtc/jsep/${peer}`;
        return this.delete(url);
    }

    // --------------------------
    // Plugins/VMS/Devices/Events
    // --------------------------

    getVmsDeviceEventsTimesPdateOffset(
        group: string,
        project: string,
        device: string,
        date: string,
    ) {
        const prefix = `/plugins/vms/${group}/${project}`;
        const suffix = `/devices/${device}/events/times/${date}/offset`;
        const url = prefix + suffix;
        return this.get<Array<number>>(url);
    }

    // ----------------------------------
    // Plugins/VMS/Devices/Events/Configs
    // ----------------------------------

    getVmsDeviceEventsConfigs(
        group: string,
        project: string,
        device: string,
    ) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/events/configs`;
        return this.get<Array<VmsEventConfigA>>(url);
    }

    postVmsDeviceEventsConfigs(
        group: string,
        project: string,
        device: string,
        body: VmsCreateEventConfigQ
    ) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/events/configs`;
        return this.post(url, body);
    }

    getVmsDeviceEventsConfigsPconfig(
        group: string,
        project: string,
        device: string,
        config: string
    ) {
        const prefix = `/plugins/vms/${group}/${project}`;
        const suffix = `/devices/${device}/events/configs/${config}`;
        const url = prefix + suffix;
        return this.get<VmsEventConfigA>(url);
    }

    patchVmsDeviceEventsConfigsPconfig(
        group: string,
        project: string,
        device: string,
        config: string,
        body: VmsUpdateEventConfigQ,
    ) {
        const prefix = `/plugins/vms/${group}/${project}`;
        const suffix = `/devices/${device}/events/configs/${config}`;
        const url = prefix + suffix;
        return this.patch(url, body);
    }

    deleteVmsDeviceEventsConfigsPconfig(
        group: string,
        project: string,
        device: string,
        config: string,
    ) {
        const prefix = `/plugins/vms/${group}/${project}`;
        const suffix = `/devices/${device}/events/configs/${config}`;
        const url = prefix + suffix;
        return this.delete(url);
    }

    // -----------------------------
    // Plugins/VMS/Devices/Debugging
    // -----------------------------

    postVmsDeviceProcessDebugStart(group: string, project: string, device: string) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/start`;
        return this.post(url);
    }

    postVmsDeviceProcessDebugStop(group: string, project: string, device: string) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/stop`;
        return this.post(url);
    }

    postVmsDeviceProcessDebugEventColor(
        group: string, project: string, device: string, body: VmsEventConfigColorQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/color`;
        return this.post(url, body);
    }

    postVmsDeviceProcessDebugEventDetection(
        group: string, project: string, device: string, body: VmsEventConfigDetectionQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/detection`;
        return this.post(url, body);
    }

    postVmsDeviceProcessDebugEventMatching(
        group: string, project: string, device: string, body: VmsEventConfigMatchingQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/matching`;
        return this.post(url, body);
    }

    getVmsDeviceProcessDebugEventMatchingTrainSnapshots(
        group: string, project: string, device: string
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/matching/train/snapshots`;
        return this.get<Array<string>>(url);
    }

    postVmsDeviceProcessDebugEventMatchingTrainSnapshots(
        group: string, project: string, device: string, body: VmsUploadImageQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/matching/train/snapshots`;
        return this.post<VmsUploadImageA>(url, body);
    }

    getVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
        group: string, project: string, device: string, snapshot: string
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const suffix_url = `/process/debug/event/matching/train/snapshots/${snapshot}`;
        return this.get<VmsImageA>(device_prefix + suffix_url);
    }

    deleteVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
        group: string, project: string, device: string, snapshot: string
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const suffix_url = `/process/debug/event/matching/train/snapshots/${snapshot}`;
        const url = device_prefix + suffix_url;
        return this.delete(url);
    }

    postVmsDeviceProcessDebugEventOcr(
        group: string, project: string, device: string, body: VmsEventConfigOcrQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/ocr`;
        return this.post(url, body);
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

    getVmsEventsSnapshotsPevent(group: string, project: string, event: string) {
        const url = `/plugins/vms/${group}/${project}/events/snapshots/${event}`;
        return this.get<VmsEventImageA>(url);
    }

    getVmsEventsThumbnailsPevent(group: string, project: string, event: string) {
        const url = `/plugins/vms/${group}/${project}/events/thumbnails/${event}`;
        return this.get<VmsEventImageA>(url);
    }

    postVmsEventsFilter(group: string, project: string, body: VmsFilterEventQ) {
        const url = `/plugins/vms/${group}/${project}/events/filter`;
        return this.post<Array<VmsEventA>>(url, body);
    }

    postVmsEventsNews(group: string, project: string, body: VmsNewsEventQ) {
        const url = `/plugins/vms/${group}/${project}/events/news`;
        return this.post<Array<VmsEventA>>(url, body);
    }

    postVmsEventsLatest(group: string, project: string, body: VmsLatestEventQ) {
        const url = `/plugins/vms/${group}/${project}/events/latest`;
        return this.post<Array<VmsEventA>>(url, body);
    }

    getVmsEventsDates(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/events/dates`;
        return this.get<Array<string>>(url);
    }

    getVmsEventsDevices(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/events/devices`;
        return this.get<Array<number>>(url);
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

    // ------------------
    // Plugins/VMS/Record
    // ------------------

    getVmsRecordsPdeviceDates(
        group: string,
        project: string,
        device: string,
    ) {
        const url = `/plugins/vms/${group}/${project}/records/${device}/dates`;
        return this.get<Array<string>>(url);
    }

    urlVmsRecordsPdevicePlaylistMaster(
        group: string,
        project: string,
        device: string,
        start: string,
        last: string,
    ) {
        const url = `/plugins/vms/${group}/${project}/records/${device}/playlist/master`;
        const params = `?start=${start}&last=${last}`;
        return this.baseURL + url + params;
    }

    getVmsRecordsPdeviceRangesPdate(
        group: string,
        project: string,
        device: string,
        date: string,
    ) {
        const url = `/plugins/vms/${group}/${project}/records/${device}/ranges/${date}`;
        return this.get<Array<VmsRecordRangeA>>(url);
    }
};
