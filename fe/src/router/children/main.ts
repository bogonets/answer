import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainMembers from '@/pages/main/MainMembers.vue';
import MainSettings from '@/pages/main/MainSettings.vue';
import MainTables from '@/pages/main/MainTables.vue';
import MainVms from '@/pages/main/MainVms.vue';

// Airjoy
import AirJoyManage from '@/components/external/airjoy/AirJoyManage.vue';
import AirjoyMonitor from '@/components/external/airjoy/AirjoyMonitor.vue';
import AirJoyGraph from '@/components/external/airjoy/AirJoyGraph.vue';

export const mainChildren = [
    {
        path: ':group/:project/dashboard',
        component: MainDashboard,
        name: mainNames.mainDashboard,
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
        path: ':group/:project/vms',
        component: MainVms,
        name: mainNames.mainVms,
    },

    // Airjoy
    {
        path: ':group/:project/airjoy/summary',
        component: AirJoyManage,
        name: mainNames.airjoySummary,
    },
    {
        path: ':group/:project/airjoy/monitor',
        component: AirjoyMonitor,
        name: mainNames.airjoyMonitor,
    },
    {
        path: ':group/:project/airjoy/graph',
        component: AirJoyGraph,
        name: mainNames.airJoyGraph,
    },
];

export default mainChildren;
