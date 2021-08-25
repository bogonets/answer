import adminNames from '@/router/names/admin';
import devNames from '@/router/names/dev';
import groupNames from '@/router/names/group';
import rootNames from '@/router/names/root';
import selfNames from '@/router/names/self';

export const names = {
    // errorNotFound: 'ErrorNotFound',
    // about: 'About',
    //
    // dev: 'Dev',
    // devOverview: 'DevOverview',
    //
    // // REFACTORING BEGIN ---
    // mainDashboard: 'MainDashboard',
    // mainProjectConfigs: 'MainProjectConfigs',
    // mainProjectMembers: 'MainProjectMembers',
    // mainProjectAirjoyTables: 'MainProjectAirjoyTables',
    // mainProjectAirjoyStatistics: 'MainProjectAirjoyStatistics',
    // mainProjectAirjoyMonitoring: 'MainProjectAirjoyMonitoring',
    // mainProjectDashboard: 'MainProjectDashboard',
    // mainProjectFiles: 'MainProjectFiles',
    // mainProjectLayouts: 'MainProjectLayouts',
    // mainProjectsNew: 'MainProjectsNew',
    // mainProjects: 'MainProjects',
    // mainProjectTables: 'MainProjectTables',
    // mainProjectTasks: 'MainProjectTasks',
    // mainProjectVisualProgramming: 'MainProjectVisualProgramming',
    // mainProjectVms: 'MainProjectVms',
    // mainProject: 'MainProject',
    // // END ---
    //
    // groups: 'Groups',
    //
    // main: 'RouterBarMain',
    // mainOverview: 'MainOverview',
    // mainGroup: 'RouterNaviGroup',
    // mainGroupMembers: 'MainGroupMembers',
    // mainGroupProjects: 'MainGroupProjects',
    // mainGroupSettings: 'mainGroupSettings',
    // mainGroups: 'Groups.vue',
    // mainGroupsNew: 'GroupsNew.vue',

    ...adminNames,
    ...devNames,
    ...groupNames,
    ...rootNames,
    ...selfNames,
};

export default names;
