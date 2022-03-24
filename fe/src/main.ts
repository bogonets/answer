import Vue from 'vue';
import App from './App.vue';
import '@/registerServiceWorker';
import router from '@/router';
import vuetify from '@/plugins/vuetify';
import '@/plugins/chart.js';
import 'roboto-fontface/css/roboto/roboto-fontface.css';
import '@fortawesome/fontawesome-free/css/all.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import '@/styles/font-face-nanum.css';
import '@/toast';

import {LocalStore} from '@/store/LocalStore';
import {sessionStore} from '@/store';
Vue.prototype.$store = sessionStore;

import i18n from '@/translations';

import VueApiV2 from '@/apis';
Vue.use(VueApiV2);

import VueVersions from '@/versions';
Vue.use(VueVersions);

import {publicPath as PUBLIC_PATH} from '@/../vue.config';

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const localStore = Vue.prototype.$localStore as LocalStore;
    if (!localStore.access) {
      next(`${PUBLIC_PATH}signin`);
    } else {
      next();
    }
  } else {
    next();
  }
});

new Vue({
  router,
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#app');
