import devNames from '@/router/names/dev';
import DevEnvs from '@/pages/dev/DevEnvs.vue';
import DevInfos from '@/pages/dev/DevInfos.vue';
import DevOverview from '@/pages/dev/DevOverview.vue';

export const devChildren = [
    {
        path: 'envs',
        component: DevEnvs,
        name: devNames.devEnvs,
    },
    {
        path: 'infos',
        component: DevInfos,
        name: devNames.devInfos,
    },
    {
        path: 'overview',
        component: DevOverview,
        name: devNames.devOverview,
    },
];

export default devChildren;
