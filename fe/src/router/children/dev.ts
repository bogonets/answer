import devNames from '@/router/names/dev';
import Dev from '@/pages/dev/Dev.vue';
import DevEnvs from '@/pages/dev/DevEnvs.vue';

export const devChildren = [
    {
        path: '',
        component: Dev,
        name: devNames.dev,
    },
    {
        path: 'envs',
        component: DevEnvs,
        name: devNames.devEnvs,
    },
];

export default devChildren;
