import { Vue, Watch } from 'vue-property-decorator';
import { RawLocation } from 'vue-router';
import VisualMain from "@/pages/_main/project/setting/vgMain.vue";
import AirJoyManage from "@/components/external/airjoy/AirJoyManage.vue";
import AirJoyGraph from "@/components/external/airjoy/AirJoyGraph.vue";
import AirJoyMonitor from "@/components/external/airjoy/AirjoyMonitor.vue";
import ProjectDashboardPage from "@/pages/main/project/ProjectDashboardPage.vue";
import LayoutsPage from "@/pages/main/project/LayoutsPage.vue";
import TablesPage from "@/pages/main/project/TablesPage.vue";
import FilesPage from "@/pages/main/project/FilesPage.vue";
import TasksPage from "@/pages/main/project/TasksPage.vue";
import VmsPage from "@/pages/main/project/VmsPage.vue";

export default class VueBase extends Vue {

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

    moveTo(location: RawLocation) {
        if (this.$router.currentRoute.path === location.toString()) {
            return;
        }

        this.$router.push(location).catch((reason: any) => {
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

    moveToMainConfigAdminUsersEdit(username: string) {
        const prefix = this.paths.mainConfigAdminUsersEdit;
        this.moveTo(`${prefix}?username=${username}`);
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
