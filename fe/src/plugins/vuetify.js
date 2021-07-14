import Vue from "vue";
import Vuetify from "vuetify/lib";
import { Ripple, Resize } from "vuetify/lib/directives";

Vue.use(Vuetify);
Vue.directive("ripple", Ripple);
Vue.directive("v-resize", Resize);

export default new Vuetify({
  theme: {
    light: true,
    dark: true,
  }
});
