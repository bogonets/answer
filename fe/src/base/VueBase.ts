import Component, {mixins} from 'vue-class-component';
import Toast from '@/base/mixin/Toast';
import WatchI18n from '@/base/mixin/WatchI18n';
import RouterAdmin from '@/base/router/RouterAdmin';
import RouterDev from '@/base/router/RouterDev';
import RouterGroup from "@/base/router/RouterGroup";
import RouterMain from '@/base/router/RouterMain';
import RouterRoot from '@/base/router/RouterRoot';
import RouterSelf from '@/base/router/RouterSelf';
import StorePermission from '@/base/store/StorePermission';
import {PLUGIN_NAME_VMS} from "@/packet/plugin";

export class PermissionError extends Error {
    constructor(message?: string) {
        super(message);
    }
}

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
    StorePermission,
) {
    getOem() {
        return this.$localStore.preference.oem;
    }

    hasAdmin() {
        return this.$localStore.user.is_admin || false;
    }

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
        const perm = await this.$api2.getSelfPermissionsPgroup(group);
        this.$sessionStore.permissionGroup = group;
        this.$sessionStore.clearPermissionProject();
        this.$sessionStore.permission = perm;
        return perm;
    }

    async requestProjectPermission() {
        const group = this.$route.params.group;
        const project = this.$route.params.project;
        const perm = await this.$api2.getSelfPermissionsPgroupPproject(group, project);
        this.$sessionStore.permissionGroup = group;
        this.$sessionStore.permissionProject = project;
        this.$sessionStore.permission = perm;
        return perm;
    }

    // hasLayoutRead() {
    //     if (!this.isLayoutRead) {
    //         this.toastError(this.$t('toast.no_layout_read').toString());
    //         throw new PermissionError('Layout write permission is required');
    //     }
    // }
    //
    // hasLayoutWrite() {
    //     if (!this.isLayoutWrite) {
    //         this.toastError(this.$t('toast.no_layout_write').toString());
    //         throw new PermissionError('Layout write permission is required');
    //     }
    // }
    //
    // hasStorageRead() {
    //     if (!this.isStorageRead) {
    //         this.toastError(this.$t('toast.no_storage_read').toString());
    //         throw new PermissionError('Storage read permission is required');
    //     }
    // }
    //
    // hasStorageWrite() {
    //     if (!this.isStorageWrite) {
    //         this.toastError(this.$t('toast.no_storage_write').toString());
    //         throw new PermissionError('Storage write permission is required');
    //     }
    // }
    //
    // hasManagerRead() {
    //     if (!this.isManagerRead) {
    //         this.toastError(this.$t('toast.no_manager_read').toString());
    //         throw new PermissionError('Manager read permission is required');
    //     }
    // }
    //
    // hasManagerWrite() {
    //     if (!this.isManagerWrite) {
    //         this.toastError(this.$t('toast.no_manager_write').toString());
    //         throw new PermissionError('Manager write permission is required');
    //     }
    // }
    //
    // hasGraphRead() {
    //     if (!this.isGraphRead) {
    //         this.toastError(this.$t('toast.no_graph_read').toString());
    //         throw new PermissionError('Graph read permission is required');
    //     }
    // }
    //
    // hasGraphWrite() {
    //     if (!this.isGraphWrite) {
    //         this.toastError(this.$t('toast.no_graph_write').toString());
    //         throw new PermissionError('Graph write permission is required');
    //     }
    // }
    //
    // hasMemberRead() {
    //     if (!this.isMemberRead) {
    //         this.toastError(this.$t('toast.no_member_read').toString());
    //         throw new PermissionError('Member read permission is required');
    //     }
    // }
    //
    // hasMemberWrite() {
    //     if (!this.isMemberWrite) {
    //         this.toastError(this.$t('toast.no_member_write').toString());
    //         throw new PermissionError('Member write permission is required');
    //     }
    // }
    //
    // hasSettingRead() {
    //     if (!this.isSettingRead) {
    //         this.toastError(this.$t('toast.no_setting_read').toString());
    //         throw new PermissionError('Setting read permission is required');
    //     }
    // }
    //
    // hasSettingWrite() {
    //     if (!this.isSettingWrite) {
    //         this.toastError(this.$t('toast.no_setting_write').toString());
    //         throw new PermissionError('Setting write permission is required');
    //     }
    // }
}
