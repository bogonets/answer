import {mixins} from 'vue-class-component';
import {Component, Watch} from 'vue-property-decorator';
// import {Vue, Component, Watch, Emit} from 'vue-property-decorator';
// import {RawLocation} from 'vue-router';
// import {Names} from '@/router/names';
// import SimpleToast from '@/components/SimpleToast.vue';
// import MainProjectMembers from "@/components/external/airjoy/AuthManagement.vue";
// import AirJoyManage from "@/components/external/airjoy/AirJoyManage.vue";
// import AirJoyGraph from "@/components/external/airjoy/AirJoyGraph.vue";
// import AirJoyMonitor from "@/components/external/airjoy/AirjoyMonitor.vue";

import Toast from '@/base/mixin/Toast';
import WatchI18n from '@/base/mixin/WatchI18n';
import RouterAdmin from '@/base/router/RouterAdmin';
import RouterDev from '@/base/router/RouterDev';
import RouterGroup from "@/base/router/RouterGroup";
import RouterRoot from '@/base/router/RouterRoot';
import RouterSelf from '@/base/router/RouterSelf';

@Component
export default class VueBase extends mixins(
    Toast,
    WatchI18n,
    RouterAdmin,
    RouterDev,
    RouterGroup,
    RouterRoot,
    RouterSelf,
) {
    moveToMainGroups() {
    }

    moveToMainGroupsNew() {
    }

    moveToMainProjects() {
    }

    moveToMainProjectsNew() {
    }

    moveToMainProjectMembers() {
    }

    moveToMainProject(group?: string, project?: string) {
    }

    // simpleToast(message: any, detail?: any) {
    //     return {
    //         component: SimpleToast,
    //         props: {
    //             message: message?.toString() || '',
    //             detail: detail?.toString() || '',
    //         },
    //         listeners: {
    //             click: () => {},
    //         },
    //     };
    // }
    //
    // toastSuccess(message: any, detail?: any) {
    //     this.$toast.success(this.simpleToast(message, detail));
    // }
    //
    // toastInfo(message: any, detail?: any) {
    //     this.$toast.info(this.simpleToast(message, detail));
    // }
    //
    // toastWarning(message: any, detail?: any) {
    //     this.$toast.warning(this.simpleToast(message, detail));
    // }
    //
    // toastError(message: any, detail?: any) {
    //     this.$toast.error(this.simpleToast(message, detail));
    // }
    //
    // toastRequestSuccess() {
    //     this.toastSuccess(this.$t('toast.request_success').toString());
    // }
    //
    // toastRequestFailure(error?) {
    //     const message = this.$t('toast.request_failure').toString();
    //     if (!error) {
    //         this.toastError(message);
    //         return;
    //     }
    //
    //     if (typeof error.response !== 'undefined') {
    //         const code = error.response.status;
    //         const reason = error.response.statusText;
    //         this.toastError(message, `[${code}] ${reason}`);
    //     } else {
    //         this.toastError(message, error.toString());
    //     }
    // }
    //
    // // ------
    // // Router
    // // ------
    //
    // moveToBack() {
    //     this.$router.back();
    // }
    //
    // moveTo(name: string, params?: object) {
    //     if (this.$router.currentRoute.name === name) {
    //         return;
    //     }
    //
    //     const rawLocation = {
    //         name: name,
    //         params: params,
    //     } as RawLocation;
    //
    //     this.$router.push(rawLocation).catch((reason: any) => {
    //         if (reason.name !== 'NavigationDuplicated') {
    //             throw reason;
    //         }
    //     })
    // }

    // // ----
    // // Self
    // // ----
    //
    // moveToSelf() {
    //     this.moveTo(this.routeNames.self);
    // }
    //
    // moveToSelfAppearance() {
    //     this.moveTo(this.routeNames.selfAppearance);
    // }
    //
    // // -----
    // // About
    // // -----
    //
    // moveToAbout() {
    //     this.moveTo(this.routeNames.about);
    // }
    //
    // // ----
    // // Main
    // // ----
    //
    // moveToGroups() {
    //     this.moveTo(this.routeNames.groups);
    // }
    //
    // moveToMain() {
    //     this.moveTo(this.routeNames.main);
    // }
    //
    // moveToMainGroups() {
    //     this.moveTo(this.routeNames.mainGroups);
    // }
    //
    // moveToMainGroup(group?: string) {
    //     const params = {
    //         group: group || this.$route.params.group,
    //     };
    //     this.moveTo(this.routeNames.mainGroup, params);
    // }
    //
    // moveToMainGroupMembers(group?: string) {
    //     const params = {
    //         group: group || this.$route.params.group,
    //     };
    //     this.moveTo(this.routeNames.mainGroupMembers, params);
    // }
    //
    // moveToMainGroupProjects(group?: string) {
    //     const params = {
    //         group: group || this.$route.params.group,
    //     };
    //     this.moveTo(this.routeNames.mainGroupProjects, params);
    // }
    //
    // moveToMainGroupSettings(group?: string) {
    //     const params = {
    //         group: group || this.$route.params.group,
    //     };
    //     this.moveTo(this.routeNames.mainGroupSettings, params);
    // }
    //
    // // ---------------------------------------------------------------------------------
    //
    // moveToMainDashboard() {
    //     this.moveTo(this.routeNames.mainDashboard);
    // }
    //
    // moveToMainDevTools() {
    //     this.moveTo(this.routeNames.dev);
    // }
    //
    // moveToMainGroupsNew() {
    //     this.moveTo(this.routeNames.mainGroupsNew);
    // }
    //
    // moveToMainProjectConfigs() {
    //     this.moveTo(this.routeNames.mainProjectConfigs);
    // }
    //
    // moveToMainProjectDashboard() {
    //     this.moveTo(this.routeNames.mainProjectDashboard);
    // }
    //
    // moveToMainProjectFiles() {
    //     this.moveTo(this.routeNames.mainProjectFiles);
    // }
    //
    // moveToMainProjectLayouts() {
    //     this.moveTo(this.routeNames.mainProjectLayouts);
    // }
    //
    // moveToMainProjectsNew() {
    //     this.moveTo(this.routeNames.mainProjectsNew);
    // }
    //
    // moveToMainProjects(group?: string) {
    //     const params = {
    //         group: group || this.$route.params.group,
    //     };
    //     this.moveTo(this.routeNames.mainProjects, params);
    // }
    //
    // moveToMainProjectTables() {
    //     this.moveTo(this.routeNames.mainProjectTables);
    // }
    //
    // moveToMainProjectTasks() {
    //     this.moveTo(this.routeNames.mainProjectTasks);
    // }
    //
    // moveToMainProjectVisualProgramming() {
    //     this.moveTo(this.routeNames.mainProjectVisualProgramming);
    // }
    //
    // moveToMainProjectVms() {
    //     this.moveTo(this.routeNames.mainProjectVms);
    // }
    //
    // moveToMainProject(group?: string, project?: string) {
    //     const params = {
    //         group: group || this.$route.params.group,
    //         project: project || this.$route.params.project,
    //     };
    //     this.moveTo(this.routeNames.mainProject, params);
    // }
    //
    // // --- refactoring begin ---
    //
    // moveToMainProjectMembers() {
    //     this.moveTo(this.routeNames.mainProjectMembers);
    // }
    //
    // moveToMainProjectAirjoyTables() {
    //     this.moveTo(this.routeNames.mainProjectAirjoyTables);
    // }
    //
    // moveToMainProjectAirjoyStatistics() {
    //     this.moveTo(this.routeNames.mainProjectAirjoyStatistics);
    // }
    //
    // moveToMainProjectAirjoyMonitoring() {
    //     this.moveTo(this.routeNames.mainProjectAirjoyMonitoring);
    // }
    //
    // // --- refactoring end ---
    //
    // moveToSignin() {
    //     this.moveTo(this.routeNames.signin);
    // }
    //
    // moveToSignup() {
    //     this.moveTo(this.routeNames.signup);
    // }
    //
    // moveToSignupAdmin() {
    //     this.moveTo(this.routeNames.init);
    // }
    //
    // moveToRoot() {
    //     this.moveToSignin();
    // }
}
