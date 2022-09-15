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

// REMOVE
import MainDatasets from '@/pages/main/MainDatasets.vue';
import MainLabel from '@/pages/main/MainLabel.vue';
import MainCategory from '@/pages/main/MainCategory.vue';
import MainInstructions from '@/pages/main/MainInstructions.vue';
import MainMachineLearning from '@/pages/main/MainMachineLearning.vue';
import MainStorage from '@/pages/main/MainStorage.vue';
import MainHooks from '@/pages/main/MainHooks.vue';
import MainToolSettings from '@/pages/main/MainToolSettings.vue';

// External
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

  // REMOVE
  {
    path: ':group/:project/datasets',
    component: MainDatasets,
    name: mainNames.mainDatasets,
  },
  {
    path: ':group/:project/label',
    component: MainLabel,
    name: mainNames.mainLabel,
  },
  {
    path: ':group/:project/category',
    component: MainCategory,
    name: mainNames.mainCategory,
  },
  {
    path: ':group/:project/instructions',
    component: MainInstructions,
    name: mainNames.mainInstructions,
  },
  {
    path: ':group/:project/ml',
    component: MainMachineLearning,
    name: mainNames.mainMachineLearning,
  },
  {
    path: ':group/:project/storage',
    component: MainStorage,
    name: mainNames.mainStorage,
  },
  {
    path: ':group/:project/hooks',
    component: MainHooks,
    name: mainNames.mainHooks,
  },
  {
    path: ':group/:project/tools',
    component: MainToolSettings,
    name: mainNames.mainToolSettings,
  },
];

export default mainChildren;
