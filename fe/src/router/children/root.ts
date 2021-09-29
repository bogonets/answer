import adminChildren from '@/router/children/admin';
import devChildren from '@/router/children/dev';
import groupChildren from '@/router/children/group';
import mainChildren from '@/router/children/main';
import selfChildren from '@/router/children/self';

import rootNames from '@/router/names/root';

import RouterBarMain from '@/pages/router/RouterBarMain.vue';
import RouterNaviAdmin from '@/pages/router/RouterNaviAdmin.vue';
import RouterNaviDev from '@/pages/router/RouterNaviDev.vue';
import RouterNaviGroup from '@/pages/router/RouterNaviGroup.vue';
import RouterNaviMain from '@/pages/router/RouterNaviMain.vue';
import RouterNaviSelf from '@/pages/router/RouterNaviSelf.vue';

import Root from '@/pages/Root.vue';
import Init from '@/pages/Init.vue';
import Signin from '@/pages/Signin.vue';
import Signup from '@/pages/Signup.vue';
import Error from '@/pages/Error.vue';

import RootGroups from '@/pages/RootGroups.vue';
import RootGroupsNew from '@/pages/RootGroupsNew.vue';
import RootProjects from '@/pages/RootProjects.vue';
import RootProjectsNew from '@/pages/RootProjectsNew.vue';
import RootAbout from '@/pages/RootAbout.vue';

import PUBLIC_PATH from '@/router/public-path';

export const rootChildren = [
    {
        path: PUBLIC_PATH + 'init',
        component: Init,
        name: rootNames.init,
    },
    {
        path: PUBLIC_PATH + 'signin',
        component: Signin,
        name: rootNames.signin,
    },
    {
        path: PUBLIC_PATH + 'signup',
        component: Signup,
        name: rootNames.signup,
    },
    {
        path: PUBLIC_PATH,
        component: RouterBarMain,
        meta: {requiresAuth: true},
        children: [
            {
                path: '',
                component: Root,
                name: rootNames.root,
            },
            {
                path: 'groups',
                component: RootGroups,
                name: rootNames.rootGroups,
            },
            {
                path: 'groups/new',
                component: RootGroupsNew,
                name: rootNames.rootGroupsNew,
            },
            {
                path: 'projects',
                component: RootProjects,
                name: rootNames.rootProjects,
            },
            {
                path: 'projects/new',
                component: RootProjectsNew,
                name: rootNames.rootProjectsNew,
            },
            {
                path: 'group',
                component: RouterNaviGroup,
                children: groupChildren,
            },
            {
                path: 'main',
                component: RouterNaviMain,
                children: mainChildren,
            },
            {
                path: 'self',
                component: RouterNaviSelf,
                children: selfChildren,
            },
            {
                path: 'admin',
                component: RouterNaviAdmin,
                children: adminChildren,
            },
            {
                path: 'dev',
                component: RouterNaviDev,
                children: devChildren,
            },
            {
                path: 'about',
                component: RootAbout,
                name: rootNames.rootAbout,
            },
        ]
    },
    {
        path: '*',
        component: Error,
    }
];

export default rootChildren;
