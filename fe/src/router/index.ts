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
import AccountPage from '@/pages/main/config/account/AccountPage.vue';
import AdminPage from '@/pages/main/config/admin/AdminPage.vue';
import OverviewPage from '@/pages/main/config/admin/OverviewPage.vue';
import MainDashboardPage from '@/pages/main/MainDashboardPage.vue';
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
import ProjectsNewPage from '@/pages/main/ProjectsNewPage.vue';
import TablesPage from "@/pages/main/project/TablesPage.vue";
import FilesPage from "@/pages/main/project/FilesPage.vue";
import TasksPage from "@/pages/main/project/TasksPage.vue";
import VmsPage from "@/pages/main/project/VmsPage.vue";
import LayoutsPage from "@/pages/main/project/LayoutsPage.vue";
import ProjectDashboardPage from "@/pages/main/project/ProjectDashboardPage.vue";
import VisualProgrammingPage from "@/pages/main/project/VisualProgrammingPage.vue";
import ProjectSettingsPage from "@/pages/main/project/ProjectSettingsPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: LoginPage,
    name: LoginPage.name,
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
    component: MainPage,
    name: MainPage.name,
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
        component: MainDashboardPage,
        name: MainDashboardPage.name,
      },
      {
        path: 'config/account',
        component: AccountPage,
        name: AccountPage.name,
        children: [
          {
            path: '',
            redirect: 'appearance',
          },
          {
            path: 'appearance',
            component: AppearancePage,
            name: AppearancePage.name,
          },
        ]
      },
      {
        path: 'config/admin',
        component: AdminPage,
        name: AdminPage.name,
        children: [
          {
            path: '',
            redirect: 'overview',
          },
          {
            path: 'overview',
            component: OverviewPage,
            name: OverviewPage.name,
          },
          {
            path: 'users',
            component: UsersPage,
            name: UsersPage.name,
          },
          {
            path: 'users/new',
            component: UsersNewPage,
            name: UsersNewPage.name,
          },
          {
            path: 'users/edit',
            component: UsersEditPage,
            name: UsersEditPage.name,
          },
          {
            path: 'groups',
            component: GroupsPage,
            name: GroupsPage.name,
          },
          {
            path: 'features',
            component: FeaturesPage,
            name: FeaturesPage.name,
          },
          {
            path: 'settings',
            component: SettingsPage,
            name: SettingsPage.name,
          },
          {
            path: 'lambdas',
            component: LambdasPage,
            name: LambdasPage.name,
          },
        ]
      },
      {
        path: 'dev',
        component: DevelopmentToolsPage,
        name: DevelopmentToolsPage.name,
      },
      {
        path: 'about',
        component: AboutPage,
        name: AboutPage.name,
      },
      {
        path: 'projects',
        component: ProjectsPage,
        name: ProjectsPage.name,
      },
      {
        path: 'projects/new',
        component: ProjectsNewPage,
        name: ProjectsNewPage.name,
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
            component: ProjectDashboardPage,
            name: ProjectDashboardPage.name,
          },
          {
            path: 'layouts',
            component: LayoutsPage,
            name: LayoutsPage.name,
          },
          {
            path: 'tables',
            component: TablesPage,
            name: TablesPage.name,
          },
          {
            path: 'files',
            component: FilesPage,
            name: FilesPage.name,
          },
          {
            path: 'tasks',
            component: TasksPage,
            name: TasksPage.name,
          },
          {
            path: 'vp',
            component: VisualProgrammingPage,
            name: VisualProgrammingPage.name,
          },
          {
            path: 'vms',
            component: VmsPage,
            name: VmsPage.name,
          },
          {
            path: 'settings',
            component: ProjectSettingsPage,
            name: ProjectSettingsPage.name,
          },
          {
            path: 'auth_management',
            component: AuthManagement,
            name: AuthManagement.name,
          },
          {
            path: 'version',
            component: Version,
            name: Version.name,
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
