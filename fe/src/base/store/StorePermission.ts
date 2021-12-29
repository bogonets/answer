import {Vue, Component} from 'vue-property-decorator';
import {
    PERMISSION_SLUG_RECC_DOMAIN_DELETE,
    PERMISSION_SLUG_RECC_DOMAIN_GRAPH_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_GRAPH_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_MANAGER_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MANAGER_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_MEMBER_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_SETTING_VIEW,
    PERMISSION_SLUG_RECC_DOMAIN_STORAGE_EDIT,
    PERMISSION_SLUG_RECC_DOMAIN_STORAGE_VIEW
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

    hasPermissionStorageView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_STORAGE_VIEW);
    }

    hasPermissionStorageEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_STORAGE_EDIT);
    }

    hasPermissionManagerView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_MANAGER_VIEW);
    }

    hasPermissionManagerEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_MANAGER_EDIT);
    }

    hasPermissionGraphView() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_GRAPH_VIEW);
    }

    hasPermissionGraphEdit() {
        return this.hasPermission(PERMISSION_SLUG_RECC_DOMAIN_GRAPH_EDIT);
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
}
