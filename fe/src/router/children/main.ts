import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainFiles from '@/pages/main/MainFiles.vue';
import MainKanban from '@/pages/main/MainKanban.vue';
import MainLayouts from '@/pages/main/MainLayouts.vue';
import MainMembers from '@/pages/main/MainMembers.vue';
import MainPlugin from '@/pages/main/MainPlugin.vue';
import MainSettings from '@/pages/main/MainSettings.vue';
import MainTables from '@/pages/main/MainTables.vue';
import MainTasks from '@/pages/main/MainTasks.vue';
import MainVisualProgramming from '@/pages/main/MainVisualProgramming.vue';

// External
import mainAirjoyChildren from '@/router/children/external/airjoy/main';
import RootGroups from '@/pages/RootGroups.vue';
import rootNames from '@/router/names/root';

export const mainChildren = [
  {
    path: ':group/:project/dashboard',
    component: MainDashboard,
    name: mainNames.mainDashboard,
  },
  {
    path: ':group/:project/kanban',
    component: MainKanban,
    name: mainNames.mainKanban,
  },
  {
    path: ':group/:project/files',
    component: MainFiles,
    name: mainNames.mainFiles,
  },
  {
    path: ':group/:project/layouts',
    component: MainLayouts,
    name: mainNames.mainLayouts,
  },
  {
    path: ':group/:project/members',
    component: MainMembers,
    name: mainNames.mainMembers,
  },
  {
    path: ':group/:project/plugins/:plugin/:menu',
    component: MainPlugin,
    name: mainNames.mainPlugin,
  },
  {
    path: ':group/:project/settings',
    component: MainSettings,
    name: mainNames.mainSettings,
  },
  {
    path: ':group/:project/tables',
    component: MainTables,
    name: mainNames.mainTables,
  },
  {
    path: ':group/:project/tasks',
    component: MainTasks,
    name: mainNames.mainTasks,
  },
  {
    path: ':group/:project/vp',
    component: MainVisualProgramming,
    name: mainNames.mainVisualProgramming,
  },

  ...mainAirjoyChildren,
];

export default mainChildren;
