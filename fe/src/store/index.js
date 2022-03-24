import Vue from 'vue';
import Vuex from 'vuex';
import { vuexSessionStorage } from './persist';
import modules from './modules';
import VueLocalStore from'@/store/LocalStore';
import VueSessionStore from'@/store/SessionStore';

Vue.use(Vuex);
Vue.use(VueLocalStore);
Vue.use(VueSessionStore);

const ENABLE_STRICT = process.env.NODE_ENV !== 'production';

export const sessionStore = new Vuex.Store({
  modules,
  strict: ENABLE_STRICT,
  plugins: [vuexSessionStorage.plugin],
});
