import mainAirjoyNames from '@/router/names/external/airjoy/main';
import MainAirjoyChart from '@/pages/external/airjoy/main/MainAirjoyChart.vue';
import MainAirjoyDetails from '@/pages/external/airjoy/main/MainAirjoyDetails.vue';
import MainAirjoyDevices from '@/pages/external/airjoy/main/MainAirjoyDevices.vue';
import MainAirjoyLive from '@/pages/external/airjoy/main/MainAirjoyLive.vue';
import MainAirjoyService from '@/pages/external/airjoy/main/MainAirjoyService.vue';
import MainAirjoySettings from '@/pages/external/airjoy/main/MainAirjoySettings.vue';
import MainAirjoySummary from '@/pages/external/airjoy/main/MainAirjoySummary.vue';

export const mainAirjoyChildren = [
    {
        path: ':group/:project/airjoy/chart/:device',
        component: MainAirjoyChart,
        name: mainAirjoyNames.mainAirjoyChart,
    },
    {
        path: ':group/:project/airjoy/details/:device',
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
        path: ':group/:project/airjoy/service/:device',
        component: MainAirjoyService,
        name: mainAirjoyNames.mainAirjoyService,
    },
    {
        path: ':group/:project/airjoy/settings',
        component: MainAirjoySettings,
        name: mainAirjoyNames.mainAirjoySettings,
    },
    {
        path: ':group/:project/airjoy/summary',
        component: MainAirjoySummary,
        name: mainAirjoyNames.mainAirjoySummary,
    },
];

export default mainAirjoyChildren;
