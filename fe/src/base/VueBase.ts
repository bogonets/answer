import Component, {mixins} from 'vue-class-component';
import Toast from '@/base/mixin/Toast';
import WatchI18n from '@/base/mixin/WatchI18n';
import RouterAdmin from '@/base/router/RouterAdmin';
import RouterDev from '@/base/router/RouterDev';
import RouterGroup from "@/base/router/RouterGroup";
import RouterMain from '@/base/router/RouterMain';
import RouterRoot from '@/base/router/RouterRoot';
import RouterSelf from '@/base/router/RouterSelf';

@Component
export default class VueBase extends mixins(
    Toast,
    WatchI18n,
    RouterAdmin,
    RouterDev,
    RouterGroup,
    RouterMain,
    RouterRoot,
    RouterSelf,
) {
    moveToMainGroups() {
    }

    moveToMainProjects() {
    }

    moveToMainProjectsNew() {
    }

    moveToMainProject(group?: string, project?: string) {
    }

    async requestGroupPermission() {
        const group = this.$route.params.group;
        const perm = await this.$api2.getMainPermissionsPgroup(group);
        this.$sessionStore.permissionGroup = group;
        this.$sessionStore.clearPermissionProject();
        this.$sessionStore.permission = perm;
        return perm;
    }

    async requestProjectPermission() {
        const group = this.$route.params.group;
        const project = this.$route.params.project;
        const perm = await this.$api2.getMainPermissionsPgroupPproject(group, project);
        this.$sessionStore.permissionGroup = group;
        this.$sessionStore.permissionProject = project;
        this.$sessionStore.permission = perm;
        return perm;
    }
}
