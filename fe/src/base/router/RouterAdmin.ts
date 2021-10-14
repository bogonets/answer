import Component, {mixins} from 'vue-class-component';
import RouterAdminAirjoy from '@/base/router/external/airjoy/RouterAdminAirjoy';
import adminNames from '@/router/names/admin';

@Component
export default class RouterAdmin extends mixins(RouterAdminAirjoy) {
    moveToAdmin() {
        this.moveToAdminOverview();
    }

    moveToAdminConfigs() {
        this.moveTo(adminNames.adminConfigs);
    }

    moveToAdminContainers() {
        this.moveTo(adminNames.adminContainers);
    }

    moveToAdminGroups() {
        this.moveTo(adminNames.adminGroups);
    }

    moveToAdminGroupsEdit(group: string) {
        this.moveTo(adminNames.adminGroupsEdit, {group});
    }

    moveToAdminGroupsNew() {
        this.moveTo(adminNames.adminGroupsNew);
    }

    moveToAdminOverview() {
        this.moveTo(adminNames.adminOverview);
    }

    moveToAdminPermissions() {
        this.moveTo(adminNames.adminPermissions);
    }

    moveToAdminPermissionsEdit(perm: string) {
        this.moveTo(adminNames.adminPermissionsEdit, {perm});
    }

    moveToAdminPermissionsNew() {
        this.moveTo(adminNames.adminPermissionsNew);
    }

    moveToAdminProjects() {
        this.moveTo(adminNames.adminProjects);
    }

    moveToAdminProjectsEdit(group: string, project: string) {
        this.moveTo(adminNames.adminProjectsEdit, {group, project});
    }

    moveToAdminProjectsNew(group?: string) {
        const params = {group: group || ''};
        this.moveTo(adminNames.adminProjectsNew, params);
    }

    moveToAdminTemplates() {
        this.moveTo(adminNames.adminTemplates);
    }

    moveToAdminUsers() {
        this.moveTo(adminNames.adminUsers);
    }

    moveToAdminUsersEdit(username: string) {
        this.moveTo(adminNames.adminUsersEdit, {username});
    }

    moveToAdminUsersNew() {
        this.moveTo(adminNames.adminUsersNew);
    }

    moveToAdminVmsDevices() {
        this.moveTo(adminNames.adminVmsDevices);
    }

    moveToAdminVmsDevicesDiscovery() {
        this.moveTo(adminNames.adminVmsDevicesDiscovery);
    }

    moveToAdminVmsDevicesNew() {
        this.moveTo(adminNames.adminVmsDevicesNew);
    }
}
