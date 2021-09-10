import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainMembers from '@/pages/main/MainMembers.vue';
import MainSettings from '@/pages/main/MainSettings.vue';
import MainTables from '@/pages/main/MainTables.vue';
import MainVms from '@/pages/main/MainVms.vue';

// External
import mainAirjoyChildren from '@/router/children/external/airjoy/main';

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

    ...mainAirjoyChildren,
];

export default mainChildren;
