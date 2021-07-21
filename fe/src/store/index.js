import Vue from 'vue';
import Vuex from 'vuex';
import { vuexSessionStorage } from './persist';
import modules from './modules';
import VueLocalStore from'@/store/LocalStore';

Vue.use(Vuex);
Vue.use(VueLocalStore);

const ENABLE_STRICT = process.env.NODE_ENV !== 'production';

export const sessionStore = new Vuex.Store({
  modules,
  strict: ENABLE_STRICT,
  plugins: [vuexSessionStorage.plugin],
});

export const templateStore = new Vuex.Store({
  state: {
    lambdaTemplates: {},
  },
  getters: {
    getLambdaTemplates: function(state) {
      return state.lambdaTemplates;
    },
  },
  mutations: {
    setLambdaTemplates(state, templates) {
      state.lambdaTemplates = templates;
    },
  },
});
