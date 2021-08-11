import Names from '@/router/names';

// import GuideLayout from '@/pages/_main/project/layout/LayoutGuide.vue';
// import LayoutMain from '@/pages/_main/project/layout/LayoutMain.vue';
// import VisualMain from '@/pages/_main/project/setting/vgMain.vue';
// import StorageMain from '@/pages/_main/project/storage/StorageMain.vue';

import Error from '@/pages/Error.vue';
import MainAbout from '@/pages/MainAbout.vue';
import MainAccountAppearance from '@/pages/MainAccountAppearance.vue';
import MainAccount from '@/pages/MainAccount.vue';
import MainAdminEnvs from '@/pages/MainAdminEnvs.vue';
import MainAdminFeatures from '@/pages/MainAdminFeatures.vue';
import MainAdminGroups from '@/pages/MainAdminGroups.vue';
import MainAdminLambdas from '@/pages/MainAdminLambdas.vue';
import MainAdminOverview from '@/pages/MainAdminOverview.vue';
import MainAdminUsersEdit from '@/pages/MainAdminUsersEdit.vue';
import MainAdminUsersNew from '@/pages/MainAdminUsersNew.vue';
import MainAdminUsers from '@/pages/MainAdminUsers.vue';
import MainAdmin from '@/pages/MainAdmin.vue';
import MainDashboard from '@/pages/MainDashboard.vue';
import MainDevTools from '@/pages/MainDevTools.vue';
import MainGroups from '@/pages/MainGroups.vue';
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

export const mainAdminChildren = [
    {
        path: '',
        name: Names.mainAdmin,
        redirect: 'overview',
    },
    {
        path: 'overview',
        component: MainAdminOverview,
        name: Names.mainAdminOverview,
    },
    {
        path: 'users',
        component: MainAdminUsers,
        name: Names.mainAdminUsers,
    },
    {
        path: 'users/new',
        component: MainAdminUsersNew,
        name: Names.mainAdminUsersNew,
    },
    {
        path: 'users/edit',
        component: MainAdminUsersEdit,
        name: Names.mainAdminUsersEdit,
    },
    {
        path: 'groups',
        component: MainAdminGroups,
        name: Names.mainAdminGroups,
    },
    {
        path: 'features',
        component: MainAdminFeatures,
        name: Names.mainAdminFeatures,
    },
    {
        path: 'settings',
        component: MainAdminEnvs,
        name: Names.mainAdminEnvs,
    },
    {
        path: 'lambdas',
        component: MainAdminLambdas,
        name: Names.mainAdminLambdas,
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
    //     path: 'auth_management',
    //     component: AuthManagement,
    //     name: AuthManagement.name,
    // },
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
    // {
    //     path: 'airjoy_manage',
    //     component: AirJoyManage,
    //     name: AirJoyManage.name,
    // },
    // {
    //     path: 'airjoy_graph',
    //     component: AirJoyGraph,
    //     name: AirJoyGraph.name,
    // },
    // {
    //     path: 'airjoy_monitor',
    //     component: AirJoyMonitor,
    //     name: AirJoyMonitor.name,
    // },
];

export const mainChildren = [
    {
        path: '',
        name: Names.main,
        redirect: 'dashboard',
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
    {
        path: 'admin',
        component: MainAdmin,
        children: mainAdminChildren,
    },
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
        path: '*',
        component: Error,
        name: Names.errorNotFound,
    }
];

export default Routes;
