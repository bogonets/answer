import Names from '@/router/names';

// import GuideLayout from '@/pages/_main/project/layout/LayoutGuide.vue';
// import LayoutMain from '@/pages/_main/project/layout/LayoutMain.vue';
// import VisualMain from '@/pages/_main/project/setting/vgMain.vue';
// import StorageMain from '@/pages/_main/project/storage/StorageMain.vue';

import Error from '@/pages/Error.vue';
import MainAbout from '@/pages/MainAbout.vue';
import MainAccountAppearance from '@/pages/MainAccountAppearance.vue';
import MainAccount from '@/pages/MainAccount.vue';
import AdminInfos from '@/pages/AdminInfos.vue';
import AdminConfigs from '@/pages/AdminConfigs.vue';
import AdminGroups from '@/pages/AdminGroups.vue';
import AdminGroupsEdit from '@/pages/AdminGroupsEdit.vue';
import AdminGroupsNew from '@/pages/AdminGroupsNew.vue';
import AdminTemplates from '@/pages/AdminTemplates.vue';
import AdminOverview from '@/pages/AdminOverview.vue';
import AdminPermissions from '@/pages/AdminPermissions.vue';
import AdminPermissionsNew from '@/pages/AdminPermissionsNew.vue';
import AdminPermissionsEdit from '@/pages/AdminPermissionsEdit.vue';
import AdminProjects from '@/pages/AdminProjects.vue';
import AdminProjectsNew from '@/pages/AdminProjectsNew.vue';
import AdminProjectsEdit from '@/pages/AdminProjectsEdit.vue';
import AdminTasks from '@/pages/AdminTasks.vue';
import AdminUsers from '@/pages/AdminUsers.vue';
import AdminUsersEdit from '@/pages/AdminUsersEdit.vue';
import AdminUsersNew from '@/pages/AdminUsersNew.vue';
import Admin from '@/pages/Admin.vue';
import MainDashboard from '@/pages/MainDashboard.vue';
import MainDevTools from '@/pages/MainDevTools.vue';
import MainGroups from '@/pages/MainGroups.vue';
import MainGroupsNew from '@/pages/MainGroupsNew.vue';
import MainProjectConfigs from '@/pages/MainProjectConfigs.vue';
import MainProjectDashboard from '@/pages/MainProjectDashboard.vue';
import MainProjectFiles from '@/pages/MainProjectFiles.vue';
import MainProjectLayouts from '@/pages/MainProjectLayouts.vue';
import MainProjectsNew from '@/pages/MainProjectsNew.vue';
import MainProjects from '@/pages/MainProjects.vue';
import MainProjectTables from '@/pages/MainProjectTables.vue';
import MainProjectTasks from '@/pages/MainProjectTasks.vue';
import MainProjectVisualProgramming from '@/pages/MainProjectVisualProgramming.vue';
import MainProjectVms from '@/pages/MainProjectVms.vue';
import MainProject from '@/pages/MainProject.vue';
import Main from '@/pages/Main.vue';
import Signin from '@/pages/Signin.vue';
import SignupAdmin from '@/pages/SignupAdmin.vue';
import Signup from '@/pages/Signup.vue';

import MainProjectMembers from '@/components/external/airjoy/AuthManagement.vue';
import AirJoyManage from '@/components/external/airjoy/AirJoyManage.vue';
import AirJoyGraph from '@/components/external/airjoy/AirJoyGraph.vue';
import AirJoyMonitor from '@/components/external/airjoy/AirjoyMonitor.vue';

export const mainAccountChildren = [
    {
        path: '',
        name: Names.mainAccount,
        redirect: 'appearance',
    },
    {
        path: 'appearance',
        component: MainAccountAppearance,
        name: Names.mainAccountAppearance,
    },
];

export const adminChildren = [
    {
        path: '',
        name: Names.admin,
        redirect: 'overview',
    },
    {
        path: 'overview',
        component: AdminOverview,
        name: Names.adminOverview,
    },
    {
        path: 'users',
        component: AdminUsers,
        name: Names.adminUsers,
    },
    {
        path: 'users/new',
        component: AdminUsersNew,
        name: Names.adminUsersNew,
    },
    {
        path: 'users/edit',
        component: AdminUsersEdit,
        name: Names.adminUsersEdit,
    },
    {
        path: 'groups',
        component: AdminGroups,
        name: Names.adminGroups,
    },
    {
        path: 'groups/new',
        component: AdminGroupsNew,
        name: Names.adminGroupsNew,
    },
    {
        path: 'groups/edit',
        component: AdminGroupsEdit,
        name: Names.adminGroupsEdit,
    },
    {
        path: 'permissions',
        component: AdminPermissions,
        name: Names.adminPermissions,
    },
    {
        path: 'permissions/new',
        component: AdminPermissionsNew,
        name: Names.adminPermissionsNew,
    },
    {
        path: 'permissions/edit',
        component: AdminPermissionsEdit,
        name: Names.adminPermissionsEdit,
    },
    {
        path: 'projects',
        component: AdminProjects,
        name: Names.adminProjects,
    },
    {
        path: 'projects/new',
        component: AdminProjectsNew,
        name: Names.adminProjectsNew,
    },
    {
        path: 'projects/edit',
        component: AdminProjectsEdit,
        name: Names.adminProjectsEdit,
    },
    {
        path: 'tasks',
        component: AdminTasks,
        name: Names.adminTasks,
    },
    {
        path: 'configs',
        component: AdminConfigs,
        name: Names.adminConfigs,
    },
    {
        path: 'infos',
        component: AdminInfos,
        name: Names.adminInfos,
    },
    {
        path: 'lamdas',
        component: AdminTemplates,
        name: Names.adminLamdas,
    },
]

export const mainProjectChildren = [
    {
        path: '',
        name: Names.mainProject,
        redirect: 'dashboard',
    },
    {
        path: 'dashboard',
        component: MainProjectDashboard,
        name: Names.mainProjectDashboard,
    },
    {
        path: 'layouts',
        component: MainProjectLayouts,
        name: Names.mainProjectLayouts,
    },
    {
        path: 'tables',
        component: MainProjectTables,
        name: Names.mainProjectTables,
    },
    {
        path: 'files',
        component: MainProjectFiles,
        name: Names.mainProjectFiles,
    },
    {
        path: 'tasks',
        component: MainProjectTasks,
        name: Names.mainProjectTasks,
    },
    {
        path: 'vp',
        component: MainProjectVisualProgramming,
        name: Names.mainProjectVisualProgramming,
    },
    {
        path: 'vms',
        component: MainProjectVms,
        name: Names.mainProjectVms,
    },
    {
        path: 'settings',
        component: MainProjectConfigs,
        name: Names.mainProjectConfigs,
    },
    // {
    //     path: 'guide_layout',
    //     component: GuideLayout,
    //     name: Names.mainProjectGuideLayout,
    // },
    // {
    //     path: 'layout/:name',
    //     component: LayoutMain,
    //     name: LayoutMain.name,
    // },
    // {
    //     path: 'storage',
    //     component: StorageMain,
    //     name: StorageMain.name,
    // },
    // {
    //     path: 'graph_setting',
    //     component: VisualMain,
    //     name: VisualMain.name,
    // },
    {
        path: 'auth_management',
        component: MainProjectMembers,
        name: Names.mainProjectMembers,
    },
    {
        path: 'airjoy_manage',
        component: AirJoyManage,
        name: Names.mainProjectAirjoyTables,
    },
    {
        path: 'airjoy_graph',
        component: AirJoyGraph,
        name: Names.mainProjectAirjoyStatistics,
    },
    {
        path: 'airjoy_monitor',
        component: AirJoyMonitor,
        name: Names.mainProjectAirjoyMonitoring,
    },
];

export const mainChildren = [
    {
        path: '',
        name: Names.main,
        redirect: 'groups',
    },
    {
        path: 'dashboard',
        component: MainDashboard,
        name: Names.mainDashboard,
    },
    {
        path: 'account',
        component: MainAccount,
        children: mainAccountChildren,
    },
    // {
    //     path: 'admin',
    //     component: MainAdmin,
    //     children: mainAdminChildren,
    // },
    {
        path: 'dev',
        component: MainDevTools,
        name: Names.mainDevTools,
    },
    {
        path: 'about',
        component: MainAbout,
        name: Names.mainAbout,
    },
    {
        path: 'projects',
        component: MainProjects,
        name: Names.mainProjects,
    },
    {
        path: 'projects/new',
        component: MainProjectsNew,
        name: Names.mainProjectsNew,
    },
    {
        path: 'project/:group/:project',
        component: MainProject,
        children: mainProjectChildren,
    },
    {
        path: 'groups',
        component: MainGroups,
        name: Names.mainGroups,
    },
    {
        path: 'groups/new',
        component: MainGroupsNew,
        name: Names.mainGroupsNew,
    },
];

export const Routes = [
    {
        path: '/',
        component: Signin,
        name: Names.signin,
    },
    {
        path: '/signup',
        component: Signup,
        name: Names.signup,
    },
    {
        path: '/signup/admin',
        component: SignupAdmin,
        name: Names.signupAdmin,
    },
    {
        path: '/main',
        component: Main,
        meta: {requiresAuth: true},
        children: mainChildren,
    },
    {
        path: '/admin',
        component: Admin,
        meta: {requiresAuth: true},
        children: adminChildren,
    },
    {
        path: '*',
        component: Error,
        name: Names.errorNotFound,
    }
];

export default Routes;
