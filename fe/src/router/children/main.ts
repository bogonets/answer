import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainMembers from '@/pages/main/MainMembers.vue';
import MainSettings from '@/pages/main/MainSettings.vue';
import MainTables from '@/pages/main/MainTables.vue';
import MainVms from '@/pages/main/MainVms.vue';

// Airjoy
import AirjoyChart from '@/pages/main/airjoy/AirjoyChart.vue';
import AirjoyLive from '@/pages/main/airjoy/AirjoyLive.vue';
import AirjoySummary from '@/pages/main/airjoy/AirjoySummary.vue';
import AirjoyTable from '@/pages/main/airjoy/AirjoyTable.vue';

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
        path: ':group/:project/airjoy/chart',
        component: AirjoyChart,
        name: mainNames.mainAirjoyChart,
    },
    {
        path: ':group/:project/airjoy/live',
        component: AirjoyLive,
        name: mainNames.mainAirjoyLive,
    },
    {
        path: ':group/:project/airjoy/summary',
        component: AirjoySummary,
        name: mainNames.mainAirjoySummary,
    },
    {
        path: ':group/:project/airjoy/table',
        component: AirjoyTable,
        name: mainNames.mainAirjoyTable,
    },
];

export default mainChildren;
