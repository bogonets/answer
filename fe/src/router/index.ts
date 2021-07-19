import Vue from "vue";
import Router from "vue-router";

// import MainPage from '@/pages/Main/Main.vue'
import LoginPage from "@/pages/LoginPage.vue";
import Signup from "@/pages/Login/SignUp.vue";
import SignupAdmin from "@/pages/Login/SignUpAdmin.vue";

import MainPage from "@/pages/MainPage.vue";

import ProjectsMain from "@/pages/Main/projects/ProjectsMain.vue";

import Project from "@/pages/Main/project/ProjectMain.vue";
import GuideLayout from "@/pages/Main/project/layout/LayoutGuide.vue";
import LayoutMain from "@/pages/Main/project/layout/LayoutMain.vue";
import VisualMain from "@/pages/Main/project/setting/vgMain.vue";
import StorageMain from "@/pages/Main/project/storage/StorageMain.vue";
import AirJoyManage from "@/components/external/airjoy/AirJoyManage.vue";
import AirJoyGraph from "@/components/external/airjoy/AirJoyGraph.vue";
import AirJoyMonitor from "@/components/external/airjoy/AirjoyMonitor.vue";
import AuthManagement from "@/components/external/airjoy/AuthManagement.vue"
import Version from "@/pages/Info/Version.vue";

import NotFound from "@/pages/Error/NotFound.vue";

Vue.use(Router);

const answerRoutes = [
  {
    path: "/",
    name: "Login",
    component: LoginPage,
    props: {}
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup
  },
  {
    path: "/signupadmin",
    name: "Signupadmin",
    component: SignupAdmin
  },
  {
    path: "/main",
    name: "AnswerMain",
    meta: { requiresAuth: true },
    component: MainPage,
    children: [
      {
        path: "projects",
        name: "ProjectsMain",
        component: ProjectsMain
      },
      {
        path: "project",
        name: "ProjectMain",
        component: Project,
        children: [
          {
            path: "guide_layout",
            name: "guide_layout",
            component: GuideLayout
          },
          { path: "layout/:name", name: "layout", component: LayoutMain },
          { path: "storage", name: "storage", component: StorageMain },
          {
            path: "graph_setting",
            name: "graph_setting",
            component: VisualMain
          },
          {
            path: "airjoy_manage",
            name: "airjoy_manage",
            component: AirJoyManage
          },
          {
            path: "airjoy_graph",
            name: "airjoy_graph",
            component: AirJoyGraph
          },
          {
            path: "airjoy_monitor",
            name: "airjoy_monitor",
            component: AirJoyMonitor
          },
          {
            path: "auth_management",
            name: "auth_management",
            component: AuthManagement
          },
          { path: "version", name: "Version", component: Version }
        ]
      }
    ]
  },
  {
    path: "*",
    name: "404",
    component: NotFound
  }
];

export default new Router({
  routes: answerRoutes
});
