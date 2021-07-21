import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import '@fortawesome/fontawesome-free/css/all.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import '@/styles/font-face-nanum.css'

import { sessionStore } from '@/store';
Vue.prototype.$store = sessionStore;

import i18n from '@/translations';

import { Observable, Subscription, Subject } from 'rxjs';
import VueRx from 'vue-rx';
Vue.use(VueRx, { Observable, Subscription, Subject });

// Make component.
import vCsvField from '@/components/Input/aiCsvField.vue';
import aCsvInput from '@/components/Input/aCsvInput.vue';
import aJsonField from '@/components/Input/aJsonField.vue';
import aTextarea from '@/components/Input/aTextarea.vue';
import aConsole from '@/components/Console/aConsole.vue';
import movePanel from '@/components/Dashboard/adbDashboardPanel.vue';
Vue.component('vCsvField', vCsvField);
Vue.component('aCsvInput', aCsvInput);
Vue.component('aJsonField', aJsonField);
Vue.component('aTextarea', aTextarea);
Vue.component('aConsole', aConsole);
Vue.component('movePanel', movePanel);

// Use open source component.
import VueDragDrop from 'vue-drag-drop';
import VueDraggable from 'vuedraggable';
Vue.use(VueDragDrop);
Vue.component('draggable', VueDraggable);

import WhiteBoard from '@/components/Canvas/WhiteBoard.vue';
Vue.component('white-board', WhiteBoard);

import { Splitpanes, Pane } from 'splitpanes';
import 'splitpanes/dist/splitpanes.css';
Vue.component('vSplitpanes', Splitpanes);
Vue.component('vPane', Pane);

import sha256 from 'sha256';
Vue.prototype.$sha256 = sha256;

import { REST_API } from '@/apis/api';
const restApi = REST_API();
Vue.prototype.$api = restApi;

import VueApiV2 from '@/apis';
Vue.use(VueApiV2);

import { ANSWER_UTIL } from './services/answer_util';
const answerUtil = ANSWER_UTIL();
Vue.prototype.$util = answerUtil;

Vue.config.productionTip = false;

Vue.prototype.$version = require('../package.json')['version'];
Vue.prototype.$page = {
  main: '/main',
  project: '/main/project',
  projects: '/main/projects',
  groups: '/main/gruops',
  version: '/main/version',
  signup: '/signup',
  login: '/'
};

import { templateStore } from "@/store";
Vue.prototype.$templateStore = templateStore;

// console logger.
Vue.prototype.$debug = function (filename, methods, ...args) {
  console.debug(
    this.$util.getNow(),
    '[' + filename + '::' + methods + '] [DEBUG]',
    ...args
  );
};
Vue.prototype.$info = function (filename, methods, ...args) {
  console.info(
    this.$util.getNow(),
    '[' + filename + '::' + methods + '] [INFO]',
    ...args
  );
};
Vue.prototype.$warn = function (filename, methods, ...args) {
  console.warn(
    this.$util.getNow(),
    '[' + filename + '::' + methods + '] [WARN]',
    ...args
  );
};
Vue.prototype.$error = function (filename, methods, ...args) {
  console.error(
    this.$util.getNow(),
    '[' + filename + '::' + methods + '] [ERROR]',
    ...args
  );
};

// Auth
Vue.prototype.$isAuth = function (level) {
  if (level <= this.$store.getters['project/getProjectAuth']) {
    return true;
  } else {
    return false;
  }
}

// Theme Color
Vue.prototype.$backgroundColor = function () {
  if (this.$vuetify.theme.dark) {
    return {
      'background-color': 'rgba(125, 125, 125, 0.2)',
      'color': 'white'
    }
  } else {
    return {
      'background-color': 'rgba(245, 245, 245)',
      'color': 'black'
    }
  }
}

Vue.prototype.$buttonColor = function () {
  if (this.$vuetify.theme.dark) {
    return {
      'background-color': 'rgba(66, 66, 66)',
      'color': 'white'
    }
  } else {
    return {
      'background-color': 'rgba(224, 224, 224)',
      'color': 'black'
    }
  }
}

// Router Extension
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 이 라우트는 인증이 필요하며 로그인 한 경우 확인하십시오.
    // 그렇지 않은 경우 로그인 페이지로 리디렉션하십시오.
    if (!sessionStore.getters['user/getAccessToken']) {
      next('/');
    } else {
      next();
    }
  } else {
    next(); // 반드시 next()를 호출하십시오!
  }
});

new Vue({
  router,
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#app');
