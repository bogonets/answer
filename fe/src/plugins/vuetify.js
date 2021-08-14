import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import en from 'vuetify/lib/locale/en';
import ko from 'vuetify/lib/locale/ko';
import { Ripple, Resize } from 'vuetify/lib/directives';
import '@mdi/font/css/materialdesignicons.css';  // Ensure you are using css-loader
import '@/plugins/vuetify.scss';

Vue.use(Vuetify);
Vue.directive('ripple', Ripple);
Vue.directive('v-resize', Resize);

export default new Vuetify({
  lang: {
    locales: { en, ko },
    current: 'ko',
  },
  icons: {
    iconfont: 'mdi',
  },
});
