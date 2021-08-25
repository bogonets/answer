import devNames from '@/router/names/dev';
import DevEnvs from '@/pages/dev/DevEnvs.vue';
import DevOverview from '@/pages/dev/DevOverview.vue';

export const devChildren = [
    {
        path: 'envs',
        component: DevEnvs,
        name: devNames.devEnvs,
    },
    {
        path: 'overview',
        component: DevOverview,
        name: devNames.devOverview,
    },
];

export default devChildren;
