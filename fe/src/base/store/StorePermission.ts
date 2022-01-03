import {Vue, Component} from 'vue-property-decorator';
import {
    PERMISSION_SLUG_RECC_DOMAIN_DELETE,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VMS_LIVE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VMS_LIVE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_VMS_DEVICE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VMS_DEVICE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_VMS_EVENT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_VMS_EVENT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_DEVICE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_DEVICE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_LIVE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_LIVE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_CHART_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_CHART_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_SERVICE_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_SERVICE_EDIT,
} from '@/packet/permission';

@Component
export default class StorePermission extends Vue {
    async requestGroupPermission(group?: string) {
        const groupName = group || this.$route.params.group;
        const perms = await this.$api2.getSelfPermissionsPgroup(groupName);
        this.$sessionStore.permissionGroup = groupName;
        this.$sessionStore.clearPermissionProject();
        this.$sessionStore.permissionPermissions = perms;
        return perms;
    }

    async requestProjectPermission(group?: string, project?: string) {
        const groupName = group || this.$route.params.group;
        const projectName = project || this.$route.params.project;
        const perms = await this.$api2.getSelfPermissionsPgroupPproject(
            groupName, projectName
        );
        this.$sessionStore.permissionGroup = groupName;
        this.$sessionStore.permissionProject = projectName;
        this.$sessionStore.permissionPermissions = perms;
        return perms;
    }

    isDomainGroup() {
        const group = this.$sessionStore.permissionGroup;
        const project = this.$sessionStore.permissionProject;
        return group && !project;
    }

    isDomainProject() {
        const group = this.$sessionStore.permissionGroup;
        const project = this.$sessionStore.permissionProject;
        return group && project;
    }

    hasPermission(perm: string) {
        return this.$sessionStore.permissionPermissions.includes(perm);
    }

    hasPermissionLayoutView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW);
    }

    hasPermissionLayoutEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT);
    }

    hasPermissionFileView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_FILE_VIEW);
    }

    hasPermissionFileEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_FILE_EDIT);
    }

    hasPermissionTableView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_TABLE_VIEW);
    }

    hasPermissionTableEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_TABLE_EDIT);
    }

    hasPermissionTaskView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_TASK_VIEW);
    }

    hasPermissionTaskEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_TASK_EDIT);
    }

    hasPermissionVpView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_VP_VIEW);
    }

    hasPermissionVpEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_VP_EDIT);
    }

    hasPermissionMemberView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW);
    }

    hasPermissionMemberEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT);
    }

    hasPermissionSettingView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW);
    }

    hasPermissionSettingEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT);
    }

    hasPermissionDelete() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_DELETE);
    }

    hasPermissionVmsAny() {
        const vmsPermissions = [
            PERMISSION_SLUG_RECC_DOMAIN_VMS_LIVE_VIEW,
            PERMISSION_SLUG_RECC_DOMAIN_VMS_LIVE_EDIT,
            PERMISSION_SLUG_RECC_DOMAIN_VMS_DEVICE_VIEW,
            PERMISSION_SLUG_RECC_DOMAIN_VMS_DEVICE_EDIT,
            PERMISSION_SLUG_RECC_DOMAIN_VMS_EVENT_VIEW,
            PERMISSION_SLUG_RECC_DOMAIN_VMS_EVENT_EDIT,
        ];
        const perms = this.$sessionStore.permissionPermissions;
        return perms.some(x => vmsPermissions.includes(x))
    }

    hasPermissionVmsLiveView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_VMS_LIVE_VIEW);
    }

    hasPermissionVmsLiveEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_VMS_LIVE_EDIT);
    }

    hasPermissionVmsDeviceView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_VMS_DEVICE_VIEW);
    }

    hasPermissionVmsDeviceEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_VMS_DEVICE_EDIT);
    }

    hasPermissionVmsEventView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_VMS_EVENT_VIEW);
    }

    hasPermissionVmsEventEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_VMS_EVENT_EDIT);
    }

    hasPermissionAirjoyDeviceView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_DEVICE_VIEW);
    }

    hasPermissionAirjoyDeviceEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_DEVICE_EDIT);
    }

    hasPermissionAirjoyLiveView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_LIVE_VIEW);
    }

    hasPermissionAirjoyLiveEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_LIVE_EDIT);
    }

    hasPermissionAirjoyChartView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_CHART_VIEW);
    }

    hasPermissionAirjoyChartEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_CHART_EDIT);
    }

    hasPermissionAirjoyServiceView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_SERVICE_VIEW);
    }

    hasPermissionAirjoyServiceEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_AIRJOY_SERVICE_EDIT);
    }
}
