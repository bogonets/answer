import Vue from 'vue';
import VueRouter from 'vue-router';

import Signup from '@/pages/signup/SignUp.vue';
import SignupAdmin from '@/pages/signup/SignUpAdmin.vue';
import MainProjects from '@/pages/MainProjects.vue';
import Project from '@/pages/MainProject.vue';
import GuideLayout from '@/pages/_main/project/layout/LayoutGuide.vue';
import LayoutMain from '@/pages/_main/project/layout/LayoutMain.vue';
import VisualMain from '@/pages/_main/project/setting/vgMain.vue';
import StorageMain from '@/pages/_main/project/storage/StorageMain.vue';
import AirJoyManage from '@/components/external/airjoy/AirJoyManage.vue';
import AirJoyGraph from '@/components/external/airjoy/AirJoyGraph.vue';
import AirJoyMonitor from '@/components/external/airjoy/AirjoyMonitor.vue';
import AuthManagement from '@/components/external/airjoy/AuthManagement.vue'
import Error from '@/pages/Error.vue';

import MainAbout from '@/pages/MainAbout.vue';
import MainAccount from '@/pages/MainAccount.vue';
import MainAdmin from '@/pages/MainAdmin.vue';
import MainAdminOverview from '@/pages/MainAdminOverview.vue';
import MainDashboard from '@/pages/MainDashboard.vue';
import MainDevTools from '@/pages/MainDevTools.vue';
import Signin from '@/pages/Signin.vue';
import Main from '@/pages/Main.vue';
import MainAccountAppearance from '@/pages/MainAccountAppearance.vue';
import MainAdminUsers from '@/pages/MainAdminUsers.vue';
import MainAdminGroups from '@/pages/MainAdminGroups.vue';
import MainAdminFeatures from '@/pages/MainAdminFeatures.vue';
import MainAdminEnvs from '@/pages/MainAdminEnvs.vue';
import MainAdminLambdas from '@/pages/MainAdminLambdas.vue';
import MainAdminUsersNew from '@/pages/MainAdminUsersNew.vue';
import MainAdminUsersEdit from '@/pages/MainAdminUsersEdit.vue';
import MainProjectsNew from '@/pages/MainProjectsNew.vue';
import MainProjectTables from "@/pages/MainProjectTables.vue";
import MainProjectFiles from "@/pages/MainProjectFiles.vue";
import MainProjectTasks from "@/pages/MainProjectTasks.vue";
import MainProjectVms from "@/pages/MainProjectVms.vue";
import MainProjectLayouts from "@/pages/MainProjectLayouts.vue";
import MainProjectDashboard from "@/pages/MainProjectDashboard.vue";
import MainProjectVisualProgramming from "@/pages/MainProjectVisualProgramming.vue";
import MainProjectConfigs from "@/pages/MainProjectConfigs.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: Signin,
    name: Signin.name,
  },
  {
    path: '/signup',
    component: Signup,
    name: Signup.name,
  },
  {
    path: '/signup/admin',
    component: SignupAdmin,
    name: SignupAdmin.name,
  },
  {
    path: '/main',
    component: Main,
    name: Main.name,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        redirect: 'dashboard',
      },
      {
        path: 'dashboard',
        component: MainDashboard,
        name: MainDashboard.name,
      },
      {
        path: 'config/account',
        component: MainAccount,
        name: MainAccount.name,
        children: [
          {
            path: '',
            redirect: 'appearance',
          },
          {
            path: 'appearance',
            component: MainAccountAppearance,
            name: MainAccountAppearance.name,
          },
        ]
      },
      {
        path: 'config/admin',
        component: MainAdmin,
        name: MainAdmin.name,
        children: [
          {
            path: '',
            redirect: 'overview',
          },
          {
            path: 'overview',
            component: MainAdminOverview,
            name: MainAdminOverview.name,
          },
          {
            path: 'users',
            component: MainAdminUsers,
            name: MainAdminUsers.name,
          },
          {
            path: 'users/new',
            component: MainAdminUsersNew,
            name: MainAdminUsersNew.name,
          },
          {
            path: 'users/edit',
            component: MainAdminUsersEdit,
            name: MainAdminUsersEdit.name,
          },
          {
            path: 'groups',
            component: MainAdminGroups,
            name: MainAdminGroups.name,
          },
          {
            path: 'features',
            component: MainAdminFeatures,
            name: MainAdminFeatures.name,
          },
          {
            path: 'settings',
            component: MainAdminEnvs,
            name: MainAdminEnvs.name,
          },
          {
            path: 'lambdas',
            component: MainAdminLambdas,
            name: MainAdminLambdas.name,
          },
        ]
      },
      {
        path: 'dev',
        component: MainDevTools,
        name: MainDevTools.name,
      },
      {
        path: 'about',
        component: MainAbout,
        name: MainAbout.name,
      },
      {
        path: 'projects',
        component: MainProjects,
        name: MainProjects.name,
      },
      {
        path: 'projects/new',
        component: MainProjectsNew,
        name: MainProjectsNew.name,
      },
      {
        path: 'project/:group/:project',
        component: Project,
        name: Project.name,
        children: [
          {
            path: 'guide_layout',
            component: GuideLayout,
            name: GuideLayout.name,
          },
          {
            path: 'layout/:name',
            component: LayoutMain,
            name: LayoutMain.name,
          },
          {
            path: 'storage',
            component: StorageMain,
            name: StorageMain.name,
          },
          {
            path: 'graph_setting',
            component: VisualMain,
            name: VisualMain.name,
          },
          {
            path: 'airjoy_manage',
            component: AirJoyManage,
            name: AirJoyManage.name,
          },
          {
            path: 'airjoy_graph',
            component: AirJoyGraph,
            name: AirJoyGraph.name,
          },
          {
            path: 'airjoy_monitor',
            component: AirJoyMonitor,
            name: AirJoyMonitor.name,
          },
          {
            path: '',
            redirect: 'dashboard',
          },
          {
            path: 'dashboard',
            component: MainProjectDashboard,
            name: MainProjectDashboard.name,
          },
          {
            path: 'layouts',
            component: MainProjectLayouts,
            name: MainProjectLayouts.name,
          },
          {
            path: 'tables',
            component: MainProjectTables,
            name: MainProjectTables.name,
          },
          {
            path: 'files',
            component: MainProjectFiles,
            name: MainProjectFiles.name,
          },
          {
            path: 'tasks',
            component: MainProjectTasks,
            name: MainProjectTasks.name,
          },
          {
            path: 'vp',
            component: MainProjectVisualProgramming,
            name: MainProjectVisualProgramming.name,
          },
          {
            path: 'vms',
            component: MainProjectVms,
            name: MainProjectVms.name,
          },
          {
            path: 'settings',
            component: MainProjectConfigs,
            name: MainProjectConfigs.name,
          },
          {
            path: 'auth_management',
            component: AuthManagement,
            name: AuthManagement.name,
          },
        ]
      }
    ]
  },
  {
    path: '*',
    name: '404',
    component: Error,
  }
];

console.debug(routes);

export default new VueRouter({
  routes: routes
});
