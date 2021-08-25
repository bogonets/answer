import groupNames from '@/router/names/group';
import Group from '@/pages/group/Group.vue';
import GroupProjectsNew from '@/pages/group/GroupProjectsNew.vue';
import GroupMembers from '@/pages/group/GroupMembers.vue';
import GroupSettings from '@/pages/group/GroupSettings.vue';

export const groupChildren = [
    {
        path: ':group',
        component: Group,
        name: groupNames.group,
    },
    {
        path: ':group/projects/new',
        component: GroupProjectsNew,
        name: groupNames.groupProjectsNew,
    },
    {
        path: ':group/members',
        component: GroupMembers,
        name: groupNames.groupMembers,
    },
    {
        path: ':group/settings',
        component: GroupSettings,
        name: groupNames.groupSettings,
    },
];

export default groupChildren;
