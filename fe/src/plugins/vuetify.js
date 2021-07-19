import Vue from "vue";
import Vuetify from "vuetify/lib";
import { Ripple, Resize } from "vuetify/lib/directives";
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader

Vue.use(Vuetify);
Vue.directive("ripple", Ripple);
Vue.directive("v-resize", Resize);

export default new Vuetify({
  theme: {
    light: true,
    dark: true,
  },
  icons: {
    iconfont: 'mdi',
  },
});
