import devNames from '@/router/names/dev';
import DevConfigs from '@/pages/dev/DevConfigs.vue';
import DevEnvs from '@/pages/dev/DevEnvs.vue';
import DevInfos from '@/pages/dev/DevInfos.vue';
import DevOverview from '@/pages/dev/DevOverview.vue';
import DevPlugins from '@/pages/dev/DevPlugins.vue';

export const devChildren = [
    {
        path: 'configs',
        component: DevConfigs,
        name: devNames.devConfigs,
    },
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
    {
        path: 'plugins',
        component: DevPlugins,
        name: devNames.devPlugins,
    },
];

export default devChildren;
