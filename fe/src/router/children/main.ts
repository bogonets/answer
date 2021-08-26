import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainMembers from '@/pages/main/MainMembers.vue';
import MainSettings from '@/pages/main/MainSettings.vue';
import MainVms from '@/pages/main/MainVms.vue';

export const mainChildren = [
    {
        path: ':group/:project/overview',
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
        path: ':group/:project/vms',
        component: MainVms,
        name: mainNames.mainVms,
    },
];

export default mainChildren;
