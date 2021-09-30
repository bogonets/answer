import selfNames from '@/router/names/self';
import SelfAppearance from '@/pages/self/SelfAppearance.vue';
import SelfProfile from '@/pages/self/SelfProfile.vue';

export const selfChildren = [
    {
        path: 'appearance',
        component: SelfAppearance,
        name: selfNames.selfAppearance,
    },
    {
        path: 'profile',
        component: SelfProfile,
        name: selfNames.selfProfile,
    },
];

export default selfChildren;
