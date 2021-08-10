import { Vue, Watch } from 'vue-property-decorator';
import { RawLocation } from 'vue-router';
import { User } from '@/apis/api-v2';
import {Dictionary} from 'vue-router/types/router';
import LoginPage from '@/pages/LoginPage.vue';
import MainPage from '@/pages/main/MainPage.vue';
import MainDashboardPage from '@/pages/main/MainDashboardPage.vue';
import AccountPage from '@/pages/main/config/account/AccountPage.vue';
import AppearancePage from '@/pages/main/config/account/AppearancePage.vue';
import AdminPage from '@/pages/main/config/admin/AdminPage.vue';
import OverviewPage from '@/pages/main/config/admin/OverviewPage.vue';
import UsersPage from '@/pages/main/config/admin/UsersPage.vue';
import UsersNewPage from '@/pages/main/config/admin/UsersNewPage.vue';
import UsersEditPage from '@/pages/main/config/admin/UsersEditPage.vue';
import GroupsPage from '@/pages/main/config/admin/GroupsPage.vue';
import FeaturesPage from '@/pages/main/config/admin/FeaturesPage.vue';
import SettingsPage from '@/pages/main/config/admin/SettingsPage.vue';
import LambdasPage from '@/pages/main/config/admin/LambdasPage.vue';
import DevelopmentToolsPage from '@/pages/main/DevelopmentToolsPage.vue';
import AboutPage from '@/pages/main/AboutPage.vue';
import ProjectsPage from '@/pages/main/ProjectsPage.vue';
import ProjectsNewPage from '@/pages/main/ProjectsNewPage.vue';
import ProjectPage from '@/pages/main/project/ProjectPage.vue';

export default class VueBase extends Vue {

    readonly names = {
        signup: LoginPage.name,
        main: MainPage.name,
        mainDashboard: MainDashboardPage.name,
        mainConfigAccount: AccountPage.name,
        mainConfigAccountAppearance: AppearancePage.name,
        mainConfigAdmin: AdminPage.name,
        mainConfigAdminOverview: OverviewPage.name,
        mainConfigAdminUsers: UsersPage.name,
        mainConfigAdminUsersNew: UsersNewPage.name,
        mainConfigAdminUsersEdit: UsersEditPage.name,
        mainConfigAdminGroups: GroupsPage.name,
        mainConfigAdminLambdas: LambdasPage.name,
        mainConfigAdminFeatures: FeaturesPage.name,
        mainConfigAdminSettings: SettingsPage.name,
        mainDev: DevelopmentToolsPage.name,
        mainAbout: AboutPage.name,
        mainProjects: ProjectsPage.name,
        mainProjectsNew: ProjectsNewPage.name,
        mainProject: ProjectPage.name,
    };

    readonly paths = {
        root: '/',
        signup: '/signup',
        signupAdmin: '/signup/admin',
        main: '/main',
        mainDashboard: '/main/dashboard',
        mainConfigAccount: '/main/config/account',
        mainConfigAccountAppearance: '/main/config/account/appearance',
        mainConfigAdmin: '/main/config/admin',
        mainConfigAdminOverview: '/main/config/admin/overview',
        mainConfigAdminUsers: '/main/config/admin/users',
        mainConfigAdminUsersNew: '/main/config/admin/users/new',
        mainConfigAdminUsersEdit: '/main/config/admin/users/edit',
        mainConfigAdminGroups: '/main/config/admin/groups',
        mainConfigAdminGroupsNew: '/main/config/admin/groups/new',
        mainConfigAdminGroupsEdit: '/main/config/admin/groups/edit',
        mainConfigAdminFeatures: '/main/config/admin/features',
        mainConfigAdminSettings: '/main/config/admin/settings',
        mainConfigAdminLambdas: '/main/config/admin/lambdas',
        mainDev: '/main/dev',
        mainAbout: '/main/about',
        mainProjects: '/main/projects',
        mainProjectsNew: '/main/projects/new',
        mainProjectsEdit: '/main/projects/edit',
        mainGroups: '/main/groups',
        mainProject: (group: string, project: string): string => {
            return `/main/project/${group}/${project}`;
        },
    };

    readonly mainPaths = {
        graph: '/graph_setting',
        airjoy_manage: '/airjoy_manage',
        airjoy_graph: '/airjoy_graph',
        airjoy_monitor: '/airjoy_monitor',
        dashboard: '/dashboard',
        layouts: '/layouts',
        tables: '/tables',
        files: '/files',
        tasks: '/tasks',
        vp: '/vp',
        vms: '/vms',
        auth: '/auth_management',
        settings: '/settings',
    };

    @Watch('$vuetify.lang.current')
    updateI18n(newVal: string, oldVal: string) {
        console.debug(`Update i18n: ${oldVal} -> ${newVal}`);
        this.$i18n.locale = newVal;
    }

    get currentRoutePath(): string {
        return this.$router.currentRoute.path;
    }

    moveTo(location: string, params?: Dictionary<string>) {
        if (this.$router.currentRoute.path === location) {
            return;
        }

        const rawLocation = {
            path: location,
            params: params,
        } as RawLocation;

        this.$router.push(rawLocation).catch((reason: any) => {
            if (reason.name !== 'NavigationDuplicated') {
                throw reason;
            }
        })
    }

    moveToRoot() {
        this.moveTo(this.paths.root);
    }

    moveToSignup() {
        this.moveTo(this.paths.signup);
    }

    moveToSignupAdmin() {
        this.moveTo(this.paths.signupAdmin);
    }

    moveToMain() {
        this.moveTo(this.paths.main);
    }

    moveToMainDashboard() {
        this.moveTo(this.paths.mainDashboard);
    }

    moveToMainConfigAccount() {
        this.moveTo(this.paths.mainConfigAccount);
    }

    moveToMainConfigAccountAppearance() {
        this.moveTo(this.paths.mainConfigAccountAppearance);
    }

    moveToMainConfigAdmin() {
        this.moveTo(this.paths.mainConfigAdmin);
    }

    moveToMainConfigAdminOverview() {
        this.moveTo(this.paths.mainConfigAdminOverview);
    }

    moveToMainConfigAdminUsers() {
        this.moveTo(this.paths.mainConfigAdminUsers);
    }

    moveToMainConfigAdminUsersNew() {
        this.moveTo(this.paths.mainConfigAdminUsersNew);
    }

    moveToMainConfigAdminUsersEdit(user: User) {
        this.moveTo(this.paths.mainConfigAdminUsersEdit, this.userToRouteParam(user));
    }

    userToRouteParam(user: User): Dictionary<string> {
        return {
            username: user.username || '',
            nickname: user.nickname || '',
            email: user.email || '',
            phone1: user.phone1 || '',
            phone2: user.phone2 || '',
            isAdmin: user.is_admin ? 'true' : 'false',
            createdAt: user.created_at || '',
            updatedAt: user.updated_at || '',
            lastLogin: user.last_login || '',
        };
    }

    routeParamToUser(params: Dictionary<string>): User {
        return {
            username: params.username,
            nickname: params.nickname,
            email: params.email,
            phone1: params.phone1,
            phone2: params.phone2,
            is_admin: params.isAdmin === 'true',
            created_at: params.created_at,
            updated_at: params.updated_at,
            last_login: params.last_login,
        } as User;
    }

    moveToMainConfigAdminGroups() {
        this.moveTo(this.paths.mainConfigAdminGroups);
    }

    moveToMainConfigAdminGroupsNew() {
        this.moveTo(this.paths.mainConfigAdminGroupsNew);
    }

    moveToMainConfigAdminGroupsEdit() {
        this.moveTo(this.paths.mainConfigAdminGroupsEdit);
    }

    moveToMainConfigAdminFeatures() {
        this.moveTo(this.paths.mainConfigAdminFeatures);
    }

    moveToMainConfigAdminSettings() {
        this.moveTo(this.paths.mainConfigAdminSettings);
    }

    moveToMainConfigAdminLambdas() {
        this.moveTo(this.paths.mainConfigAdminLambdas);
    }

    moveToMainDev() {
        this.moveTo(this.paths.mainDev);
    }

    moveToMainAbout() {
        this.moveTo(this.paths.mainAbout);
    }

    moveToMainProjects() {
        this.moveTo(this.paths.mainProjects);
    }

    moveToMainProjectsNew() {
        this.moveTo(this.paths.mainProjectsNew);
    }

    moveToMainGroups() {
        this.moveTo(this.paths.mainGroups);
    }

    // moveToMainProjectsEdit(group: string, project: string) {
    //     const prefix = this.paths.mainProjectsEdit;
    //     this.moveTo(`${prefix}?group=${group}&project=${project}`);
    // }

    moveToMainProject(group: string, project: string) {
        this.moveTo(this.paths.mainProject(group, project));
    }

    private get routeParamsGroup(): string {
        return this.$route.params.group;
    }

    private get routeParamsProject(): string {
        return this.$route.params.project;
    }

    moveToMainProjectSubpage(subpage: string) {
        const group = this.routeParamsGroup;
        const project = this.routeParamsProject;
        const prefix = this.paths.mainProject(group, project);
        this.moveTo(prefix + subpage);
    }

    moveToMainProjectGraph() {
        this.moveToMainProjectSubpage(this.mainPaths.graph);
    }

    moveToMainProjectAirjoyManage() {
        this.moveToMainProjectSubpage(this.mainPaths.airjoy_manage);
    }

    moveToMainProjectAirjoyGraph() {
        this.moveToMainProjectSubpage(this.mainPaths.airjoy_graph);
    }

    moveToMainProjectAirjoyMonitor() {
        this.moveToMainProjectSubpage(this.mainPaths.airjoy_monitor);
    }

    moveToMainProjectDashboard() {
        this.moveToMainProjectSubpage(this.mainPaths.dashboard);
    }

    moveToMainProjectLayouts() {
        this.moveToMainProjectSubpage(this.mainPaths.layouts);
    }

    moveToMainProjectTables() {
        this.moveToMainProjectSubpage(this.mainPaths.tables);
    }

    moveToMainProjectFiles() {
        this.moveToMainProjectSubpage(this.mainPaths.files);
    }

    moveToMainProjectTasks() {
        this.moveToMainProjectSubpage(this.mainPaths.tasks);
    }

    moveToMainProjectVp() {
        this.moveToMainProjectSubpage(this.mainPaths.vp);
    }

    moveToMainProjectVms() {
        this.moveToMainProjectSubpage(this.mainPaths.vms);
    }

    moveToMainProjectAuth() {
        this.moveToMainProjectSubpage(this.mainPaths.auth);
    }

    moveToMainProjectSettings() {
        this.moveToMainProjectSubpage(this.mainPaths.settings);
    }
}
