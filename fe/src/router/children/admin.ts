import adminNames from '@/router/names/admin';
import AdminConfigs from '@/pages/admin/AdminConfigs.vue';
import AdminContainers from '@/pages/admin/AdminContainers.vue';
import AdminGroups from '@/pages/admin/AdminGroups.vue';
import AdminGroupsEdit from '@/pages/admin/AdminGroupsEdit.vue';
import AdminGroupsNew from '@/pages/admin/AdminGroupsNew.vue';
import AdminOverview from '@/pages/admin/AdminOverview.vue';
import AdminPermissions from '@/pages/admin/AdminPermissions.vue';
import AdminPermissionsEdit from '@/pages/admin/AdminPermissionsEdit.vue';
import AdminPermissionsNew from '@/pages/admin/AdminPermissionsNew.vue';
import AdminProjects from '@/pages/admin/AdminProjects.vue';
import AdminProjectsEdit from '@/pages/admin/AdminProjectsEdit.vue';
import AdminProjectsNew from '@/pages/admin/AdminProjectsNew.vue';
import AdminTemplates from '@/pages/admin/AdminTemplates.vue';
import AdminUsers from '@/pages/admin/AdminUsers.vue';
import AdminUsersEdit from '@/pages/admin/AdminUsersEdit.vue';
import AdminUsersNew from '@/pages/admin/AdminUsersNew.vue';
import AdminVmsDevices from '@/pages/admin/AdminVmsDevices.vue';
import AdminVmsDevicesDiscovery from '@/pages/admin/AdminVmsDevicesDiscovery.vue';
import AdminVmsDevicesNew from '@/pages/admin/AdminVmsDevicesNew.vue';

// External
import adminAirjoyChildren from '@/router/children/external/airjoy/admin';

export const adminChildren = [
    {
        path: 'configs',
        component: AdminConfigs,
        name: adminNames.adminConfigs,
    },
    {
        path: 'groups',
        component: AdminGroups,
        name: adminNames.adminGroups,
    },
    {
        path: 'groups/edit/:group',
        component: AdminGroupsEdit,
        name: adminNames.adminGroupsEdit,
    },
    {
        path: 'groups/new',
        component: AdminGroupsNew,
        name: adminNames.adminGroupsNew,
    },
    {
        path: 'overview',
        name: adminNames.adminOverview,
        component: AdminOverview,
    },
    {
        path: 'permissions',
        component: AdminPermissions,
        name: adminNames.adminPermissions,
    },
    {
        path: 'permissions/edit/:perm',
        component: AdminPermissionsEdit,
        name: adminNames.adminPermissionsEdit,
    },
    {
        path: 'permissions/new',
        component: AdminPermissionsNew,
        name: adminNames.adminPermissionsNew,
    },
    {
        path: 'projects',
        component: AdminProjects,
        name: adminNames.adminProjects,
    },
    {
        path: 'projects/edit/:group/:project',
        component: AdminProjectsEdit,
        name: adminNames.adminProjectsEdit,
    },
    {
        path: 'projects/new',
        component: AdminProjectsNew,
        name: adminNames.adminProjectsNew,
    },
    {
        path: 'containers',
        component: AdminContainers,
        name: adminNames.adminContainers,
    },
    {
        path: 'templates',
        component: AdminTemplates,
        name: adminNames.adminTemplates,
    },
    {
        path: 'users',
        component: AdminUsers,
        name: adminNames.adminUsers,
    },
    {
        path: 'users/edit/:username',
        component: AdminUsersEdit,
        name: adminNames.adminUsersEdit,
    },
    {
        path: 'users/new',
        component: AdminUsersNew,
        name: adminNames.adminUsersNew,
    },
    {
        path: 'vms/devices',
        component: AdminVmsDevices,
        name: adminNames.adminVmsDevices,
    },
    {
        path: 'vms/devices/discovery',
        component: AdminVmsDevicesDiscovery,
        name: adminNames.adminVmsDevicesDiscovery,
    },
    {
        path: 'vms/devices/new',
        component: AdminVmsDevicesNew,
        name: adminNames.adminVmsDevicesNew,
    },

    ...adminAirjoyChildren,
];

export default adminChildren;
