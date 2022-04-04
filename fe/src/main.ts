import Vue from 'vue';
import App from '@/App.vue';
import '@/registerServiceWorker';
import '@/plugins/chart.js';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import '@fortawesome/fontawesome-free/css/all.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import '@/styles/font-face-nanum.css';
import '@/toast';

import VueApiV2 from '@/apis';
Vue.use(VueApiV2);

import VueVersions from '@/versions';
Vue.use(VueVersions);

import Vuex from 'vuex';
import VueLocalStore from '@/store/localStore';
import VueSessionStore from '@/store/sessionStore';
Vue.use(Vuex);
Vue.use(VueLocalStore);
Vue.use(VueSessionStore);

import ResizeObserverDirective from '@/directives/ResizeObserver';
Vue.directive('resize-observer', ResizeObserverDirective);

import {LocalStore} from '@/store/localStore';
import {publicPath} from '@/../vue.config';
import i18n from '@/translations';
import vuetify from '@/plugins/vuetify';
import router from '@/router';
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const localStore = Vue.prototype.$localStore as LocalStore;
    if (!localStore.access) {
      next(`${publicPath}signin`);
    } else {
      next();
    }
  } else {
    next();
  }
});

new Vue({
  i18n,
  vuetify,
  router,
  render: h => h(App),
}).$mount('#app');
