import selfNames from '@/router/names/self';
import SelfAppearance from '@/pages/self/SelfAppearance.vue';
import SelfOverview from '@/pages/self/SelfOverview.vue';

export const selfChildren = [
    {
        path: '/appearance',
        component: SelfAppearance,
        name: selfNames.selfAppearance,
    },
    {
        path: '/overview',
        component: SelfOverview,
        name: selfNames.selfOverview,
    },
];

export default selfChildren;
