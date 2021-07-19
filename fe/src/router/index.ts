import Vue from "vue";
import Router from "vue-router";

// import MainPage from '@/pages/Main/Main.vue'
import Login from "@/pages/Login/Login.vue";
import Signup from "@/pages/Login/SignUp.vue";
import SignupAdmin from "@/pages/Login/SignUpAdmin.vue";

import MainPage from "@/pages/Main/MainPage.vue";

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
    component: Login,
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
      { path: "projects", name: "ProjectsMain", component: ProjectsMain },
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
      // isnert GroupsMain Page.
    ]
  },
  {
    path: "*",
    name: "404",
    component: NotFound
  }
];

if (process.env.NODE_ENV !== "production") {
  answerRoutes.push({
    path: "/testlist",
    name: "testlist",
    component: require("@/components/List/test/listTest.vue").default
  });
  answerRoutes.push({
    path: "/testload",
    name: "testload",
    component: require("@/components/Progress/test/loadTest.vue").default
  });
  answerRoutes.push({
    path: "/testsignupadmin",
    name: "testsignupadmin",
    component: require("@/components/Form/test/SignupAdminTest.vue").default
  });
  answerRoutes.push({
    path: "/testjsonfield",
    name: "testjsonfield",
    component: require("@/components/Input/test/jsonFieldTest.vue").default
  });
  answerRoutes.push({
    path: "/testjupyterselect",
    name: "testjupyterselect",
    component: require("@/components/Combobox/test/acbJupyterSelectTest.vue")
      .default
  });
  answerRoutes.push({
    path: "/testsimplevideo",
    name: "testsimplevideo",
    component: require("@/components/Video/Test/testSimpleVideoPlayer.vue")
      .default
  });
  answerRoutes.push({
    path: "/testusertable",
    name: "testusertable",
    component: require("@/components/Table/test/aUserTableTest.vue").default
  });
  answerRoutes.push({
    path: "/testprojecttable",
    name: "testprojecttable",
    component: require("@/components/Table/test/aProjectTableTest.vue").default
  });
  answerRoutes.push({
    path: "/testbuckettable",
    name: "testbuckettable",
    component: require("@/components/Table/test/aBucketTableTest.vue").default
  });
  answerRoutes.push({
    path: "/testbucketobjecttable",
    name: "testbucketobjecttable",
    component: require("@/components/Table/test/aBucketsObjectTableTest.vue")
      .default
  });
  answerRoutes.push({
    path: "/teststoragemanager",
    name: "teststoragemanager",
    component: require("@/components/Storage/test/aStorageManagerTest.vue")
      .default
  });
  answerRoutes.push({
    path: "/testsignup",
    name: "testsignup",
    component: require("@/components/Form/test/afSignupFormTest.vue").default
  });
  answerRoutes.push({
    path: "/testprojectmaker",
    name: "testprojectmaker",
    component: require("@/components/Form/test/afProjectMakerTest.vue").default
  });
  answerRoutes.push({
    path: "/testconsole",
    name: "testconsole",
    component: require("@/components/Console/test/aConsoleTest.vue").default
  });
  answerRoutes.push({
    path: "/testlambdainfos",
    name: "testlambdainfos",
    component: require("@/components/VisualGraph/test/vgLambdaInfoTest.vue")
      .default
  });
  answerRoutes.push({
    path: "/testlambdawidget",
    name: "testlambdawidget",
    component: require("@/components/LambdaWidget/test/lambdaWidgetsTemplate.vue")
      .default
  });
  answerRoutes.push({
    path: "/testvgsetting",
    name: "testvgsetting",
    component: require("@/components/VisualGraph/test/vgMainTest.vue").default
  });
  answerRoutes.push({
    path: "/testcsvinput",
    name: "testcsvinput",
    component: require("@/components/Input/test/aCsvInputTest.vue").default
  });
  answerRoutes.push({
    path: "/testcolorpicker",
    name: "testcolorpicker",
    component: require("@/components/Picker/test/apColorPickerTest.vue").default
  });
  answerRoutes.push({
    path: "/testblobviewer",
    name: "testblobviewer",
    component: require("@/widgets/test/acpBlobsViewer.vue").default
  });
  answerRoutes.push({
    path: "/testwhiteboard",
    name: "testwhiteboard",
    component: require("@/components/Canvas/WhiteBoard.vue").default
  });
}

export default new Router({
  routes: answerRoutes
});
