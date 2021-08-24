import Names from '@/router/names';

// import GuideLayout from '@/pages/_main/project/layout/LayoutGuide.vue';
// import LayoutMain from '@/pages/_main/project/layout/LayoutMain.vue';
// import VisualMain from '@/pages/_main/project/setting/vgMain.vue';
// import StorageMain from '@/pages/_main/project/storage/StorageMain.vue';

import Error from '@/pages/Error.vue';
import MainAbout from '@/pages/MainAbout.vue';
import SelfAppearance from '@/pages/SelfAppearance.vue';
import RouterBarMainNaviSelf from '@/pages/router/RouterBarMainNaviSelf.vue';
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
import RouterBarMainNaviAdmin from '@/pages/router/RouterBarMainNaviAdmin.vue';
import MainDashboard from '@/pages/MainDashboard.vue';
import RouterBarMainNaviDev from '@/pages/router/RouterBarMainNaviDev.vue';
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
import RouterBarMain from '@/pages/router/RouterBarMain.vue';
import Signin from '@/pages/Signin.vue';
import Init from '@/pages/Init.vue';
import Signup from '@/pages/Signup.vue';

import MainProjectMembers from '@/components/external/airjoy/AuthManagement.vue';
import AirJoyManage from '@/components/external/airjoy/AirJoyManage.vue';
import AirJoyGraph from '@/components/external/airjoy/AirJoyGraph.vue';
import AirJoyMonitor from '@/components/external/airjoy/AirjoyMonitor.vue';
import MainOverview from '@/pages/MainOverview.vue';
import RouterBarMainNaviGroup from '@/pages/router/RouterBarMainNaviGroup.vue';
import MainGroupSettings from "@/pages/MainGroupSettings.vue";
import MainGroupMembers from "@/pages/MainGroupMembers.vue";
import MainGroupProjects from "@/pages/MainGroupProjects.vue";

export const adminChildren = [
    {
        path: '',
        name: Names.admin,
        redirect: 'overview',
    },
    {
        path: 'configs',
        component: AdminConfigs,
        name: Names.adminConfigs,
    },
    {
        path: 'groups',
        component: AdminGroups,
        name: Names.adminGroups,
    },
    {
        path: 'groups/edit',
        component: AdminGroupsEdit,
        name: Names.adminGroupsEdit,
    },
    {
        path: 'groups/new',
        component: AdminGroupsNew,
        name: Names.adminGroupsNew,
    },
    {
        path: 'infos',
        component: AdminInfos,
        name: Names.adminInfos,
    },
    {
        path: 'overview',
        component: AdminOverview,
        name: Names.adminOverview,
    },
    {
        path: 'permissions',
        component: AdminPermissions,
        name: Names.adminPermissions,
    },
    {
        path: 'permissions/edit',
        component: AdminPermissionsEdit,
        name: Names.adminPermissionsEdit,
    },
    {
        path: 'permissions/new',
        component: AdminPermissionsNew,
        name: Names.adminPermissionsNew,
    },
    {
        path: 'projects',
        component: AdminProjects,
        name: Names.adminProjects,
    },
    {
        path: 'projects/edit',
        component: AdminProjectsEdit,
        name: Names.adminProjectsEdit,
    },
    {
        path: 'projects/new',
        component: AdminProjectsNew,
        name: Names.adminProjectsNew,
    },
    {
        path: 'tasks',
        component: AdminTasks,
        name: Names.adminTasks,
    },
    {
        path: 'templates',
        component: AdminTemplates,
        name: Names.adminTemplates,
    },
    {
        path: 'users',
        component: AdminUsers,
        name: Names.adminUsers,
    },
    {
        path: 'users/edit',
        component: AdminUsersEdit,
        name: Names.adminUsersEdit,
    },
    {
        path: 'users/new',
        component: AdminUsersNew,
        name: Names.adminUsersNew,
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

export const mainGroupChildren = [
    {
        path: '',
        name: Names.mainGroup,
        redirect: 'projects',
    },
    {
        path: 'members',
        component: MainGroupMembers,
        name: Names.mainGroupMembers,
    },
    {
        path: 'projects',
        component: MainGroupProjects,
        name: Names.mainGroupProjects,
    },
    {
        path: 'settings',
        component: MainGroupSettings,
        name: Names.mainGroupSettings,
    },
];

export const mainChildren = [
    {
        path: '',
        name: Names.main,
        redirect: 'groups',
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
    {
        path: 'group/:group',
        component: RouterBarMainNaviGroup,
        children: mainGroupChildren,
    },
    // {
    //     path: 'dashboard',
    //     component: MainDashboard,
    //     name: Names.mainDashboard,
    // },
    // {
    //     path: 'about',
    //     component: MainAbout,
    //     name: Names.about,
    // },
    // {
    //     path: 'projects',
    //     component: MainProjects,
    //     name: Names.mainProjects,
    // },
    // {
    //     path: 'projects/new',
    //     component: MainProjectsNew,
    //     name: Names.mainProjectsNew,
    // },
    // {
    //     path: 'project/:group/:project',
    //     component: MainProject,
    //     children: mainProjectChildren,
    // },
];

export const selfChildren = [
    {
        path: '',
        name: Names.self,
        redirect: 'appearance',
    },
    {
        path: 'appearance',
        component: SelfAppearance,
        name: Names.selfAppearance,
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
        path: '/init',
        component: Init,
        name: Names.init,
    },
    {
        path: '/main',
        component: RouterBarMain,
        meta: {requiresAuth: true},
        children: mainChildren,
    },
    {
        path: '/self',
        component: RouterBarMainNaviSelf,
        meta: {requiresAuth: true},
        children: selfChildren,
    },
    {
        path: '/admin',
        component: RouterBarMainNaviAdmin,
        meta: {requiresAuth: true},
        children: adminChildren,
    },
    {
        path: '/dev',
        component: RouterBarMainNaviDev,
        meta: {requiresAuth: true},
        name: Names.dev,
    },
    {
        path: '*',
        component: Error,
        name: Names.errorNotFound,
    }
];

export default Routes;
