import selfNames from '@/router/names/self';
import Self from '@/pages/self/Self.vue';
import SelfAppearance from '@/pages/self/SelfAppearance.vue';

export const selfChildren = [
    {
        path: '',
        component: Self,
        name: selfNames.self,
    },
    {
        path: 'appearance',
        component: SelfAppearance,
        name: selfNames.selfAppearance,
    },
];

export default selfChildren;
