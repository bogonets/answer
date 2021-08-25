// import Names from '@/router/names';
// import adminChildren from '@/router/children/admin';
// import selfChildren from '@/router/children/self';
// import groupChildren from '@/router/children/group';
// import rootChildren from '@/router/children/root';
//
// import GuideLayout from '@/pages/_main/project/layout/LayoutGuide.vue';
// import LayoutMain from '@/pages/_main/project/layout/LayoutMain.vue';
// import VisualMain from '@/pages/_main/project/setting/vgMain.vue';
// import StorageMain from '@/pages/_main/project/storage/StorageMain.vue';
// import MainAbout from '@/pages/RootAbout.vue';
// import SelfAppearance from '@/pages/self/SelfAppearance.vue';
//
// import Error from '@/pages/Error.vue';
//
// import RouterBarMain from '@/pages/router/RouterBarMain.vue';
// import RouterNaviAdmin from '@/pages/router/RouterNaviAdmin.vue';
// import RouterNaviDev from '@/pages/router/RouterNaviDev.vue';
// import RouterNaviGroup from '@/pages/router/RouterNaviGroup.vue';
// import RouterNaviSelf from '@/pages/router/RouterNaviSelf.vue';
//
// import MainDashboard from '@/pages/MainDashboard.vue';
// import Groups from '@/pages/groups/RootGroups.vue';
// import GroupsNew from '@/pages/groups/RootGroupsNew.vue';
// import MainProjectConfigs from '@/pages/MainProjectConfigs.vue';
// import MainProjectDashboard from '@/pages/MainProjectDashboard.vue';
// import MainProjectFiles from '@/pages/MainProjectFiles.vue';
// import MainProjectLayouts from '@/pages/MainProjectLayouts.vue';
// import MainProjectsNew from '@/pages/MainProjectsNew.vue';
// import MainProjects from '@/pages/MainProjects.vue';
// import MainProjectTables from '@/pages/MainProjectTables.vue';
// import MainProjectTasks from '@/pages/MainProjectTasks.vue';
// import MainProjectVisualProgramming from '@/pages/MainProjectVisualProgramming.vue';
// import MainProjectVms from '@/pages/MainProjectVms.vue';
// import MainProject from '@/pages/MainProject.vue';
// import Signin from '@/pages/Signin.vue';
// import Init from '@/pages/Init.vue';
// import Signup from '@/pages/Signup.vue';
//
// import MainProjectMembers from '@/components/external/airjoy/AuthManagement.vue';
// import AirJoyManage from '@/components/external/airjoy/AirJoyManage.vue';
// import AirJoyGraph from '@/components/external/airjoy/AirJoyGraph.vue';
// import AirJoyMonitor from '@/components/external/airjoy/AirjoyMonitor.vue';
// import MainOverview from '@/pages/MainOverview.vue';
// import RouterBarMainNaviGroup from '@/pages/router/RouterNaviGroup.vue';
// import MainGroupSettings from "@/pages/GroupSettings.vue";
// import MainGroupMembers from "@/pages/GroupMembers.vue";
// import MainGroupProjects from "@/pages/Group.vue";
//
//
// export const mainProjectChildren = [
//     {
//         path: '',
//         name: Names.mainProject,
//         redirect: 'dashboard',
//     },
//     {
//         path: 'dashboard',
//         component: MainProjectDashboard,
//         name: Names.mainProjectDashboard,
//     },
//     {
//         path: 'layouts',
//         component: MainProjectLayouts,
//         name: Names.mainProjectLayouts,
//     },
//     {
//         path: 'tables',
//         component: MainProjectTables,
//         name: Names.mainProjectTables,
//     },
//     {
//         path: 'files',
//         component: MainProjectFiles,
//         name: Names.mainProjectFiles,
//     },
//     {
//         path: 'tasks',
//         component: MainProjectTasks,
//         name: Names.mainProjectTasks,
//     },
//     {
//         path: 'vp',
//         component: MainProjectVisualProgramming,
//         name: Names.mainProjectVisualProgramming,
//     },
//     {
//         path: 'vms',
//         component: MainProjectVms,
//         name: Names.mainProjectVms,
//     },
//     {
//         path: 'settings',
//         component: MainProjectConfigs,
//         name: Names.mainProjectConfigs,
//     },
//     // {
//     //     path: 'guide_layout',
//     //     component: GuideLayout,
//     //     name: Names.mainProjectGuideLayout,
//     // },
//     // {
//     //     path: 'layout/:name',
//     //     component: LayoutMain,
//     //     name: LayoutMain.name,
//     // },
//     // {
//     //     path: 'storage',
//     //     component: StorageMain,
//     //     name: StorageMain.name,
//     // },
//     // {
//     //     path: 'graph_setting',
//     //     component: VisualMain,
//     //     name: VisualMain.name,
//     // },
//     {
//         path: 'auth_management',
//         component: MainProjectMembers,
//         name: Names.mainProjectMembers,
//     },
//     {
//         path: 'airjoy_manage',
//         component: AirJoyManage,
//         name: Names.mainProjectAirjoyTables,
//     },
//     {
//         path: 'airjoy_graph',
//         component: AirJoyGraph,
//         name: Names.mainProjectAirjoyStatistics,
//     },
//     {
//         path: 'airjoy_monitor',
//         component: AirJoyMonitor,
//         name: Names.mainProjectAirjoyMonitoring,
//     },
// ];
//
// export const mainGroupChildren = [
//     {
//         path: '',
//         name: Names.mainGroup,
//         redirect: 'projects',
//     },
//     {
//         path: 'members',
//         component: MainGroupMembers,
//         name: Names.mainGroupMembers,
//     },
//     {
//         path: 'projects',
//         component: MainGroupProjects,
//         name: Names.mainGroupProjects,
//     },
//     {
//         path: 'settings',
//         component: MainGroupSettings,
//         name: Names.mainGroupSettings,
//     },
// ];
//
// export const mainChildren = [
//     {
//         path: '',
//         name: Names.main,
//         redirect: 'groups',
//     },
//     {
//         path: 'groups',
//         component: Groups,
//         name: Names.mainGroups,
//     },
//     {
//         path: 'groups/new',
//         component: GroupsNew,
//         name: Names.mainGroupsNew,
//     },
//     {
//         path: 'group/:group',
//         component: RouterBarMainNaviGroup,
//         children: mainGroupChildren,
//     },
//     // {
//     //     path: 'dashboard',
//     //     component: MainDashboard,
//     //     name: Names.mainDashboard,
//     // },
//     // {
//     //     path: 'about',
//     //     component: MainAbout,
//     //     name: Names.about,
//     // },
//     // {
//     //     path: 'projects',
//     //     component: MainProjects,
//     //     name: Names.mainProjects,
//     // },
//     // {
//     //     path: 'projects/new',
//     //     component: MainProjectsNew,
//     //     name: Names.mainProjectsNew,
//     // },
//     // {
//     //     path: 'project/:group/:project',
//     //     component: MainProject,
//     //     children: mainProjectChildren,
//     // },
// ];

import rootChildren from '@/router/children/root';

export const routes = [
    ...rootChildren,
];

export default routes;
