import Vue from 'vue';
import VueRouter from 'vue-router';

import Signup from '@/pages/signup/SignUp.vue';
import SignupAdmin from '@/pages/signup/SignUpAdmin.vue';
import ProjectsPage from '@/pages/main/ProjectsPage.vue';
import Project from '@/pages/main/project/ProjectPage.vue';
import GuideLayout from '@/pages/_main/project/layout/LayoutGuide.vue';
import LayoutMain from '@/pages/_main/project/layout/LayoutMain.vue';
import VisualMain from '@/pages/_main/project/setting/vgMain.vue';
import StorageMain from '@/pages/_main/project/storage/StorageMain.vue';
import AirJoyManage from '@/components/external/airjoy/AirJoyManage.vue';
import AirJoyGraph from '@/components/external/airjoy/AirJoyGraph.vue';
import AirJoyMonitor from '@/components/external/airjoy/AirjoyMonitor.vue';
import AuthManagement from '@/components/external/airjoy/AuthManagement.vue'
import Version from '@/pages/Info/Version.vue';
import NotFound from '@/pages/Error/NotFound.vue';

import AboutPage from '@/pages/main/AboutPage.vue';
import ConfigAccountPage from '@/pages/main/config/ConfigAccountPage.vue';
import ConfigAdminPage from '@/pages/main/config/ConfigAdminPage.vue';
import OverviewPage from '@/pages/main/config/admin/OverviewPage.vue';
import DashboardPage from '@/pages/main/DashboardPage.vue';
import DevelopmentToolsPage from '@/pages/main/DevelopmentToolsPage.vue';
import LoginPage from '@/pages/LoginPage.vue';
import MainPage from '@/pages/main/MainPage.vue';
import AppearancePage from '@/pages/main/config/account/AppearancePage.vue';
import UsersPage from '@/pages/main/config/admin/UsersPage.vue';
import GroupsPage from '@/pages/main/config/admin/GroupsPage.vue';
import FeaturesPage from '@/pages/main/config/admin/FeaturesPage.vue';
import SettingsPage from '@/pages/main/config/admin/SettingsPage.vue';
import LambdasPage from '@/pages/main/config/admin/LambdasPage.vue';
import UsersNewPage from '@/pages/main/config/admin/UsersNewPage.vue';
import UsersEditPage from '@/pages/main/config/admin/UsersEditPage.vue';
import ProjectsEditPage from '@/pages/main/ProjectsEditPage.vue';
import ProjectsNewPage from '@/pages/main/ProjectsNewPage.vue';
import TablesPage from "@/pages/main/project/TablesPage.vue";
import FilesPage from "@/pages/main/project/FilesPage.vue";
import TasksPage from "@/pages/main/project/TasksPage.vue";
import VmsPage from "@/pages/main/project/VmsPage.vue";
import LayoutsPage from "@/pages/main/project/LayoutsPage.vue";

Vue.use(VueRouter);

const routes = [
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
        path: '',
        redirect: 'dashboard',
      },
      {
        path: 'dashboard',
        component: DashboardPage,
      },
      {
        path: 'config/account',
        component: ConfigAccountPage,
        children: [
          {
            path: '',
            redirect: 'appearance',
          },
          {
            path: 'appearance',
            component: AppearancePage,
          },
        ]
      },
      {
        path: 'config/admin',
        component: ConfigAdminPage,
        children: [
          {
            path: '',
            redirect: 'overview',
          },
          {
            path: 'overview',
            component: OverviewPage,
          },
          {
            path: 'users',
            component: UsersPage,
          },
          {
            path: 'users/new',
            component: UsersNewPage,
          },
          {
            path: 'users/edit',
            component: UsersEditPage,
            props: (route) => {
              return {
                username: route.query.username
              };
            }
          },
          {
            path: 'groups',
            component: GroupsPage,
          },
          {
            path: 'features',
            component: FeaturesPage,
          },
          {
            path: 'settings',
            component: SettingsPage,
          },
          {
            path: 'lambdas',
            component: LambdasPage,
          },
        ]
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
        component: ProjectsPage,
      },
      {
        path: 'projects/edit',
        component: ProjectsEditPage,
      },
      {
        path: 'projects/new',
        component: ProjectsNewPage,
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
            path: 'layouts',
            component: LayoutsPage,
          },
          {
            path: 'tables',
            component: TablesPage,
          },
          {
            path: 'files',
            component: FilesPage,
          },
          {
            path: 'tasks',
            component: TasksPage,
          },
          {
            path: 'vms',
            component: VmsPage,
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

export default new VueRouter({
  routes: routes
});
