import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainFiles from '@/pages/main/MainFiles.vue';
import MainLayouts from '@/pages/main/MainLayouts.vue';
import MainMembers from '@/pages/main/MainMembers.vue';
import MainSettings from '@/pages/main/MainSettings.vue';
import MainTables from '@/pages/main/MainTables.vue';
import MainTasks from '@/pages/main/MainTasks.vue';
import MainVisualProgramming from '@/pages/main/MainVisualProgramming.vue';
import MainVms from '@/pages/main/MainVms.vue';
import MainVmsLive from '@/pages/main/MainVmsLive.vue';
import MainVmsMediaSetting from '@/pages/main/MainVmsMediaSetting.vue';

// External
import mainAirjoyChildren from '@/router/children/external/airjoy/main';

export const mainChildren = [
    {
        path: ':group/:project/dashboard',
        component: MainDashboard,
        name: mainNames.mainDashboard,
    },
    {
        path: ':group/:project/files',
        component: MainFiles,
        name: mainNames.mainFiles,
    },
    {
        path: ':group/:project/layouts',
        component: MainLayouts,
        name: mainNames.mainLayouts,
    },
    {
        path: ':group/:project/members',
        component: MainMembers,
        name: mainNames.mainMembers,
    },
    {
        path: ':group/:project/settings',
        component: MainSettings,
        name: mainNames.mainSettings,
    },
    {
        path: ':group/:project/tables',
        component: MainTables,
        name: mainNames.mainTables,
    },
    {
        path: ':group/:project/tasks',
        component: MainTasks,
        name: mainNames.mainTasks,
    },
    {
        path: ':group/:project/vp',
        component: MainVisualProgramming,
        name: mainNames.mainVisualProgramming,
    },
    {
        path: ':group/:project/vms',
        component: MainVms,
        children: [
            {
                path: '',
                component: MainVmsLive,
                name: mainNames.mainVmsLive,
            },
            {
                path: ':media/setting',
                component: MainVmsMediaSetting,
                name: mainNames.mainVmsMediaSetting,
            },
        ]
    },

    ...mainAirjoyChildren,
];

export default mainChildren;
