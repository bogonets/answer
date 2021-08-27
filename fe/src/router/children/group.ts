import groupNames from '@/router/names/group';
import GroupProjects from '@/pages/group/GroupProjects.vue';
import GroupProjectsNew from '@/pages/group/GroupProjectsNew.vue';
import GroupMembers from '@/pages/group/GroupMembers.vue';
import GroupSettings from '@/pages/group/GroupSettings.vue';

export const groupChildren = [
    {
        path: '/:group/members',
        component: GroupMembers,
        name: groupNames.groupMembers,
    },
    {
        path: '/:group/projects',
        component: GroupProjects,
        name: groupNames.groupProjects,
    },
    {
        path: '/:group/projects/new',
        component: GroupProjectsNew,
        name: groupNames.groupProjectsNew,
    },
    {
        path: '/:group/settings',
        component: GroupSettings,
        name: groupNames.groupSettings,
    },
];

export default groupChildren;
