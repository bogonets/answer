import devNames from '@/router/names/dev';
import DevConfigs from '@/pages/dev/DevConfigs.vue';
import DevDaemons from '@/pages/dev/DevDaemons.vue';
import DevDaemonsEdit from '@/pages/dev/DevDaemonsEdit.vue';
import DevDaemonsNew from '@/pages/dev/DevDaemonsNew.vue';
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
        path: 'daemons',
        component: DevDaemons,
        name: devNames.devDaemons,
    },
    {
        path: 'daemons/edit/:daemon',
        component: DevDaemonsEdit,
        name: devNames.devDaemonsEdit,
    },
    {
        path: 'daemons/new',
        component: DevDaemonsNew,
        name: devNames.devDaemonsNew,
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
