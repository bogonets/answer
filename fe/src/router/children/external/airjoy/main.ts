import mainAirjoyNames from '@/router/names/external/airjoy/main';
import MainAirjoyAs from '@/pages/external/airjoy/main/MainAirjoyAs.vue';
import MainAirjoyChart from '@/pages/external/airjoy/main/MainAirjoyChart.vue';
import MainAirjoyDetails from '@/pages/external/airjoy/main/MainAirjoyDetails.vue';
import MainAirjoyDevices from '@/pages/external/airjoy/main/MainAirjoyDevices.vue';
import MainAirjoyLive from '@/pages/external/airjoy/main/MainAirjoyLive.vue';
import MainAirjoySummary from '@/pages/external/airjoy/main/MainAirjoySummary.vue';

export const mainAirjoyChildren = [
    {
        path: ':group/:project/airjoy/as/:airjoy',
        component: MainAirjoyAs,
        name: mainAirjoyNames.mainAirjoyAs,
    },
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
        path: ':group/:project/airjoy/devices',
        component: MainAirjoyDevices,
        name: mainAirjoyNames.mainAirjoyDevices,
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
];

export default mainAirjoyChildren;
