import groupNames from '@/router/names/group';
import Group from '@/pages/group/Group.vue';
import GroupMembers from '@/pages/group/GroupMembers.vue';
import GroupSettings from '@/pages/group/GroupSettings.vue';

export const groupChildren = [
    {
        path: '',
        component: Group,
        name: groupNames.group,
    },
    {
        path: 'members',
        component: GroupMembers,
        name: groupNames.groupMembers,
    },
    {
        path: 'settings',
        component: GroupSettings,
        name: groupNames.groupSettings,
    },
];

export default groupChildren;
