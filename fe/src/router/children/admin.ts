import adminNames from '@/router/names/admin';
import Admin from '@/pages/admin/Admin.vue';
import AdminConfigs from '@/pages/admin/AdminConfigs.vue';
import AdminGroups from '@/pages/admin/AdminGroups.vue';
import AdminGroupsEdit from '@/pages/admin/AdminGroupsEdit.vue';
import AdminGroupsNew from '@/pages/admin/AdminGroupsNew.vue';
import AdminInfos from '@/pages/admin/AdminInfos.vue';
import AdminPermissions from '@/pages/admin/AdminPermissions.vue';
import AdminPermissionsEdit from '@/pages/admin/AdminPermissionsEdit.vue';
import AdminPermissionsNew from '@/pages/admin/AdminPermissionsNew.vue';
import AdminProjects from '@/pages/admin/AdminProjects.vue';
import AdminProjectsEdit from '@/pages/admin/AdminProjectsEdit.vue';
import AdminProjectsNew from '@/pages/admin/AdminProjectsNew.vue';
import AdminTasks from '@/pages/admin/AdminTasks.vue';
import AdminTemplates from '@/pages/admin/AdminTemplates.vue';
import AdminUsers from '@/pages/admin/AdminUsers.vue';
import AdminUsersEdit from '@/pages/admin/AdminUsersEdit.vue';
import AdminUsersNew from '@/pages/admin/AdminUsersNew.vue';

export const adminChildren = [
    {
        path: '',
        name: adminNames.admin,
        component: Admin,
    },
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
        path: 'groups/edit',
        component: AdminGroupsEdit,
        name: adminNames.adminGroupsEdit,
    },
    {
        path: 'groups/new',
        component: AdminGroupsNew,
        name: adminNames.adminGroupsNew,
    },
    {
        path: 'infos',
        component: AdminInfos,
        name: adminNames.adminInfos,
    },
    {
        path: 'permissions',
        component: AdminPermissions,
        name: adminNames.adminPermissions,
    },
    {
        path: 'permissions/edit',
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
        path: 'projects/edit',
        component: AdminProjectsEdit,
        name: adminNames.adminProjectsEdit,
    },
    {
        path: 'projects/new',
        component: AdminProjectsNew,
        name: adminNames.adminProjectsNew,
    },
    {
        path: 'tasks',
        component: AdminTasks,
        name: adminNames.adminTasks,
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
        path: 'users/edit',
        component: AdminUsersEdit,
        name: adminNames.adminUsersEdit,
    },
    {
        path: 'users/new',
        component: AdminUsersNew,
        name: adminNames.adminUsersNew,
    },
];

export default adminChildren;
