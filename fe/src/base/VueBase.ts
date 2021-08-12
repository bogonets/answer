import {Vue, Watch} from 'vue-property-decorator';
import {RawLocation} from 'vue-router';
import {Names} from '@/router/names';
import {User, ApiV2StatusError} from '@/apis/api-v2';
import SimpleToast from '@/components/SimpleToast.vue';
import {AxiosError} from 'axios';

export default class VueBase extends Vue {

    readonly routeNames = Names;

    @Watch('$vuetify.lang.current')
    onChangeI18n(newVal: string, oldVal: string) {
        console.debug(`Change i18n: ${oldVal} -> ${newVal}`);
        this.$i18n.locale = newVal;
    }

    // -----
    // Toast
    // -----

    simpleToast(message: any, detail?: any) {
        return {
            component: SimpleToast,
            props: {
                message: message?.toString() || '',
                detail: detail?.toString() || '',
            },
            listeners: {
                click: () => {},
            },
        };
    }

    toastSuccess(message: any, detail?: any) {
        this.$toast.success(this.simpleToast(message, detail));
    }

    toastInfo(message: any, detail?: any) {
        this.$toast.info(this.simpleToast(message, detail));
    }

    toastWarning(message: any, detail?: any) {
        this.$toast.warning(this.simpleToast(message, detail));
    }

    toastError(message: any, detail?: any) {
        this.$toast.error(this.simpleToast(message, detail));
    }

    toastRequestSuccess() {
        this.toastSuccess(this.$t('toast.request_success').toString());
    }

    toastRequestFailure(error?) {
        const message = this.$t('toast.request_failure').toString();
        if (!error) {
            this.toastError(message);
            return;
        }

        if (typeof error.response !== 'undefined') {
            const code = error.response.status;
            const reason = error.response.statusText;
            this.toastError(message, `[${code}] ${reason}`);
        } else {
            this.toastError(message, error.toString());
        }
    }

    // ------
    // Router
    // ------

    get currentRoutePath(): string {
        return this.$router.currentRoute.path;
    }

    get currentRouteName(): string {
        return this.$router.currentRoute.name || '';
    }

    get currentGroupName(): string {
        return this.$route.params.group || '';
    }

    get currentProjectName(): string {
        return this.$route.params.project || '';
    }

    moveToBack() {
        this.$router.back();
    }

    moveTo(name: string, params?: object) {
        if (this.currentRouteName === name) {
            return;
        }

        const rawLocation = {
            name: name,
            params: params,
        } as RawLocation;

        this.$router.push(rawLocation).catch((reason: any) => {
            if (reason.name !== 'NavigationDuplicated') {
                throw reason;
            }
        })
    }

    moveToMainAbout() {
        this.moveTo(this.routeNames.mainAbout);
    }

    moveToMainAccountAppearance() {
        this.moveTo(this.routeNames.mainAccountAppearance);
    }

    moveToMainAccount() {
        this.moveTo(this.routeNames.mainAccount);
    }

    moveToMainAdminEnvs() {
        this.moveTo(this.routeNames.mainAdminInfos);
    }

    moveToMainAdminFeatures() {
        this.moveTo(this.routeNames.mainAdminFeatures);
    }

    moveToMainAdminGroups() {
        this.moveTo(this.routeNames.mainAdminGroups);
    }

    moveToMainAdminProjects() {
        this.moveTo(this.routeNames.mainAdminProjects);
    }

    moveToMainAdminLambdas() {
        this.moveTo(this.routeNames.mainAdminLambdas);
    }

    moveToMainAdminOverview() {
        this.moveTo(this.routeNames.mainAdminOverview);
    }

    moveToMainAdminUsersEdit(user: User) {
        this.moveTo(this.routeNames.mainAdminUsersEdit, {user: user});
    }

    moveToMainAdminUsersNew() {
        this.moveTo(this.routeNames.mainAdminUsersNew);
    }

    moveToMainAdminUsers() {
        this.moveTo(this.routeNames.mainAdminUsers);
    }

    moveToMainAdmin() {
        this.moveTo(this.routeNames.mainAdmin);
    }

    moveToMainDashboard() {
        this.moveTo(this.routeNames.mainDashboard);
    }

    moveToMainDevTools() {
        this.moveTo(this.routeNames.mainDevTools);
    }

    moveToMainGroups() {
        this.moveTo(this.routeNames.mainGroups);
    }

    moveToMainProjectConfigs() {
        this.moveTo(this.routeNames.mainProjectConfigs);
    }

    moveToMainProjectDashboard() {
        this.moveTo(this.routeNames.mainProjectDashboard);
    }

    moveToMainProjectFiles() {
        this.moveTo(this.routeNames.mainProjectFiles);
    }

    moveToMainProjectLayouts() {
        this.moveTo(this.routeNames.mainProjectLayouts);
    }

    moveToMainProjectsNew() {
        this.moveTo(this.routeNames.mainProjectsNew);
    }

    moveToMainProjects() {
        this.moveTo(this.routeNames.mainProjects);
    }

    moveToMainProjectTables() {
        this.moveTo(this.routeNames.mainProjectTables);
    }

    moveToMainProjectTasks() {
        this.moveTo(this.routeNames.mainProjectTasks);
    }

    moveToMainProjectVisualProgramming() {
        this.moveTo(this.routeNames.mainProjectVisualProgramming);
    }

    moveToMainProjectVms() {
        this.moveTo(this.routeNames.mainProjectVms);
    }

    moveToMainProject(group?: string, project?: string) {
        const params = {
            group: group || '',
            project: project || '',
        };
        this.moveTo(this.routeNames.mainProject, params);
    }

    moveToMain() {
        this.moveTo(this.routeNames.main);
    }

    moveToSignin() {
        this.moveTo(this.routeNames.signin);
    }

    moveToSignup() {
        this.moveTo(this.routeNames.signup);
    }

    moveToSignupAdmin() {
        this.moveTo(this.routeNames.signupAdmin);
    }

    moveToRoot() {
        this.moveToSignin();
    }

    // moveToMainConfigAdminUsersEdit(user: User) {
    //     this.moveTo(this.paths.mainConfigAdminUsersEdit, this.userToRouteParam(user));
    // }
    //
    // userToRouteParam(user: User): Dictionary<string> {
    //     return {
    //         username: user.username || '',
    //         nickname: user.nickname || '',
    //         email: user.email || '',
    //         phone1: user.phone1 || '',
    //         phone2: user.phone2 || '',
    //         isAdmin: user.is_admin ? 'true' : 'false',
    //         createdAt: user.created_at || '',
    //         updatedAt: user.updated_at || '',
    //         lastLogin: user.last_login || '',
    //     };
    // }
    //
    // routeParamToUser(params: Dictionary<string>): User {
    //     return {
    //         username: params.username,
    //         nickname: params.nickname,
    //         email: params.email,
    //         phone1: params.phone1,
    //         phone2: params.phone2,
    //         is_admin: params.isAdmin === 'true',
    //         created_at: params.created_at,
    //         updated_at: params.updated_at,
    //         last_login: params.last_login,
    //     } as User;
    // }
    //
    // moveToMainConfigAdminGroups() {
    //     this.moveTo(this.paths.mainConfigAdminGroups);
    // }
    //
    // moveToMainConfigAdminGroupsNew() {
    //     this.moveTo(this.paths.mainConfigAdminGroupsNew);
    // }
    //
    // moveToMainConfigAdminGroupsEdit() {
    //     this.moveTo(this.paths.mainConfigAdminGroupsEdit);
    // }
    //
    // moveToMainConfigAdminFeatures() {
    //     this.moveTo(this.paths.mainConfigAdminFeatures);
    // }
    //
    // moveToMainConfigAdminSettings() {
    //     this.moveTo(this.paths.mainConfigAdminSettings);
    // }
    //
    // moveToMainConfigAdminLambdas() {
    //     this.moveTo(this.paths.mainConfigAdminLambdas);
    // }
    //
    // moveToMainDev() {
    //     this.moveTo(this.paths.mainDev);
    // }
    //
    // moveToMainAbout() {
    //     this.moveTo(this.paths.mainAbout);
    // }
    //
    // moveToMainProjects() {
    //     this.moveTo(this.paths.mainProjects);
    // }
    //
    // moveToMainProjectsNew() {
    //     this.moveTo(this.paths.mainProjectsNew);
    // }
    //
    // moveToMainGroups() {
    //     this.moveTo(this.paths.mainGroups);
    // }
    //
    // // moveToMainProjectsEdit(group: string, project: string) {
    // //     const prefix = this.paths.mainProjectsEdit;
    // //     this.moveTo(`${prefix}?group=${group}&project=${project}`);
    // // }
    //
    // moveToMainProject(group: string, project: string) {
    //     this.moveTo(this.paths.mainProject(group, project));
    // }

    // moveToMainProjectSubpage(subpage: string) {
    //     const group = this.routeParamsGroup;
    //     const project = this.routeParamsProject;
    //     const prefix = this.paths.mainProject(group, project);
    //     this.moveTo(prefix + subpage);
    // }
    //
    // moveToMainProjectGraph() {
    //     this.moveToMainProjectSubpage(this.mainPaths.graph);
    // }
    //
    // moveToMainProjectAirjoyManage() {
    //     this.moveToMainProjectSubpage(this.mainPaths.airjoy_manage);
    // }
    //
    // moveToMainProjectAirjoyGraph() {
    //     this.moveToMainProjectSubpage(this.mainPaths.airjoy_graph);
    // }
    //
    // moveToMainProjectAirjoyMonitor() {
    //     this.moveToMainProjectSubpage(this.mainPaths.airjoy_monitor);
    // }
    //
    // moveToMainProjectDashboard() {
    //     this.moveToMainProjectSubpage(this.mainPaths.dashboard);
    // }
    //
    // moveToMainProjectLayouts() {
    //     this.moveToMainProjectSubpage(this.mainPaths.layouts);
    // }
    //
    // moveToMainProjectTables() {
    //     this.moveToMainProjectSubpage(this.mainPaths.tables);
    // }
    //
    // moveToMainProjectFiles() {
    //     this.moveToMainProjectSubpage(this.mainPaths.files);
    // }
    //
    // moveToMainProjectTasks() {
    //     this.moveToMainProjectSubpage(this.mainPaths.tasks);
    // }
    //
    // moveToMainProjectVp() {
    //     this.moveToMainProjectSubpage(this.mainPaths.vp);
    // }
    //
    // moveToMainProjectVms() {
    //     this.moveToMainProjectSubpage(this.mainPaths.vms);
    // }
    //
    // moveToMainProjectAuth() {
    //     this.moveToMainProjectSubpage(this.mainPaths.auth);
    // }
    //
    // moveToMainProjectSettings() {
    //     this.moveToMainProjectSubpage(this.mainPaths.settings);
    // }
}
