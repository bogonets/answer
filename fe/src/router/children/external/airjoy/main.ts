import mainAirjoyNames from '@/router/names/external/airjoy/main';
import MainAirjoyChart from '@/pages/external/airjoy/main/MainAirjoyChart.vue';
import MainAirjoyDetails from '@/pages/external/airjoy/main/MainAirjoyDetails.vue';
import MainAirjoyLive from '@/pages/external/airjoy/main/MainAirjoyLive.vue';
import MainAirjoySummary from '@/pages/external/airjoy/main/MainAirjoySummary.vue';
import MainAirjoyTable from '@/pages/external/airjoy/main/MainAirjoyTable.vue';

export const mainAirjoyChildren = [
    {
        path: ':group/:project/airjoy/chart/:airjoy',
        component: MainAirjoyChart,
        name: mainAirjoyNames.mainAirjoyChart,
    },
    {
        path: ':group/:project/airjoy/details/:airjoy',
        component: MainAirjoyDetails,
        name: mainAirjoyNames.mainAirjoyDetails,
    },
    {
        path: ':group/:project/airjoy/live',
        component: MainAirjoyLive,
        name: mainAirjoyNames.mainAirjoyLive,
    },
    {
        path: ':group/:project/airjoy/summary',
        component: MainAirjoySummary,
        name: mainAirjoyNames.mainAirjoySummary,
    },
    {
        path: ':group/:project/airjoy/table',
        component: MainAirjoyTable,
        name: mainAirjoyNames.mainAirjoyTable,
    },
];

export default mainAirjoyChildren;
