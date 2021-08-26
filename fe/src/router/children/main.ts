import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainVms from '@/pages/main/MainVms.vue';

export const mainChildren = [
    {
        path: ':group/:project/overview',
        component: MainDashboard,
        name: mainNames.mainDashboard,
    },
    {
        path: ':group/:project/vms',
        component: MainVms,
        name: mainNames.mainVms,
    },
];

export default mainChildren;
