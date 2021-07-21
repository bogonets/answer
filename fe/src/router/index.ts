import Vue from 'vue';
import Router from 'vue-router';

import Signup from '@/pages/Login/SignUp.vue';
import SignupAdmin from '@/pages/Login/SignUpAdmin.vue';
import ProjectsMain from '@/pages/ProjectsMain.vue';
import Project from '@/pages/Main/project/ProjectMain.vue';
import GuideLayout from '@/pages/Main/project/layout/LayoutGuide.vue';
import LayoutMain from '@/pages/Main/project/layout/LayoutMain.vue';
import VisualMain from '@/pages/Main/project/setting/vgMain.vue';
import StorageMain from '@/pages/Main/project/storage/StorageMain.vue';
import AirJoyManage from '@/components/external/airjoy/AirJoyManage.vue';
import AirJoyGraph from '@/components/external/airjoy/AirJoyGraph.vue';
import AirJoyMonitor from '@/components/external/airjoy/AirjoyMonitor.vue';
import AuthManagement from '@/components/external/airjoy/AuthManagement.vue'
import Version from '@/pages/Info/Version.vue';
import NotFound from '@/pages/Error/NotFound.vue';

import AboutPage from '@/pages/AboutPage.vue';
import ConfigAccountPage from '@/pages/ConfigAccountPage.vue';
import ConfigAdminPage from '@/pages/ConfigAdminPage.vue';
import DashboardPage from '@/pages/DashboardPage.vue';
import DevelopmentToolsPage from '@/pages/DevelopmentToolsPage.vue';
import LoginPage from '@/pages/LoginPage.vue';
import MainPage from '@/pages/MainPage.vue';

Vue.use(Router);

const answerRoutes = [
  {
    path: '/',
    component: LoginPage,
  },
  {
    path: '/signup',
    component: Signup,
  },
  {
    path: '/signup/admin',
    component: SignupAdmin,
  },
  {
    path: '/main',
    component: MainPage,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'dashboard',
        component: DashboardPage,
      },
      {
        path: 'config/account',
        component: ConfigAccountPage,
      },
      {
        path: 'config/admin',
        component: ConfigAdminPage,
      },
      {
        path: 'dev',
        component: DevelopmentToolsPage,
      },
      {
        path: 'about',
        component: AboutPage,
      },
      {
        path: 'projects',
        component: ProjectsMain,
      },
      {
        path: 'project',
        component: Project,
        children: [
          {
            path: 'guide_layout',
            component: GuideLayout,
          },
          {
            path: 'layout/:name',
            component: LayoutMain,
          },
          {
            path: 'storage',
            component: StorageMain,
          },
          {
            path: 'graph_setting',
            component: VisualMain,
          },
          {
            path: 'airjoy_manage',
            component: AirJoyManage,
          },
          {
            path: 'airjoy_graph',
            component: AirJoyGraph,
          },
          {
            path: 'airjoy_monitor',
            component: AirJoyMonitor,
          },
          {
            path: 'auth_management',
            component: AuthManagement,
          },
          {
            path: 'version',
            component: Version,
          }
        ]
      }
    ]
  },
  {
    path: '*',
    name: '404',
    component: NotFound,
  }
];

export default new Router({
  routes: answerRoutes
});
