import {Vue, Component, Watch} from 'vue-property-decorator';
import {RawLocation} from 'vue-router';
import {Names} from '@/router/names';
import SimpleToast from '@/components/SimpleToast.vue';
import MainProjectMembers from "@/components/external/airjoy/AuthManagement.vue";
import AirJoyManage from "@/components/external/airjoy/AirJoyManage.vue";
import AirJoyGraph from "@/components/external/airjoy/AirJoyGraph.vue";
import AirJoyMonitor from "@/components/external/airjoy/AirjoyMonitor.vue";

@Component
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

    moveToBack() {
        this.$router.back();
    }

    moveTo(name: string, params?: object) {
        if (this.$router.currentRoute.name === name) {
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
        this.moveTo(this.routeNames.adminInfos);
    }

    moveToMainAdminFeatures() {
        this.moveTo(this.routeNames.adminConfigs);
    }

    moveToMainAdminGroups() {
        this.moveTo(this.routeNames.adminGroups);
    }

    moveToMainAdminGroupsNew() {
        this.moveTo(this.routeNames.adminGroupsNew);
    }

    moveToMainAdminGroupsEdit(group: string) {
        this.moveTo(this.routeNames.adminGroupsEdit, {group});
    }

    moveToMainAdminPermissions() {
        this.moveTo(this.routeNames.adminPermissions);
    }

    moveToMainAdminPermissionsEdit(perm: string) {
        this.moveTo(this.routeNames.adminPermissionsEdit, {perm});
    }

    moveToMainAdminPermissionsNew() {
        this.moveTo(this.routeNames.adminPermissionsNew);
    }

    moveToMainAdminProjects() {
        this.moveTo(this.routeNames.adminProjects);
    }

    moveToMainAdminProjectsEdit(group: string, project: string) {
        this.moveTo(this.routeNames.adminProjectsEdit, {group, project});
    }

    moveToMainAdminProjectsNew(group?: string) {
        this.moveTo(this.routeNames.adminProjectsNew, {group});
    }

    moveToMainAdminTasks() {
        this.moveTo(this.routeNames.adminTasks);
    }

    moveToMainAdminTemplates() {
        this.moveTo(this.routeNames.adminLamdas);
    }

    moveToMainAdminOverview() {
        this.moveTo(this.routeNames.adminOverview);
    }

    moveToMainAdminUsersEdit(username: string) {
        this.moveTo(this.routeNames.adminUsersEdit, {username: username});
    }

    moveToMainAdminUsersNew() {
        this.moveTo(this.routeNames.adminUsersNew);
    }

    moveToMainAdminUsers() {
        this.moveTo(this.routeNames.adminUsers);
    }

    moveToMainAdmin() {
        this.moveTo(this.routeNames.admin);
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

    moveToMainGroupsNew() {
        this.moveTo(this.routeNames.mainGroupsNew);
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

    moveToMainProjects(group?: string) {
        const params = {
            group: group || this.$route.params.group,
        };
        this.moveTo(this.routeNames.mainProjects, params);
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
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(this.routeNames.mainProject, params);
    }

    // --- refactoring begin ---

    moveToMainProjectMembers() {
        this.moveTo(this.routeNames.mainProjectMembers);
    }

    moveToMainProjectAirjoyTables() {
        this.moveTo(this.routeNames.mainProjectAirjoyTables);
    }

    moveToMainProjectAirjoyStatistics() {
        this.moveTo(this.routeNames.mainProjectAirjoyStatistics);
    }

    moveToMainProjectAirjoyMonitoring() {
        this.moveTo(this.routeNames.mainProjectAirjoyMonitoring);
    }

    // --- refactoring end ---

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
}
