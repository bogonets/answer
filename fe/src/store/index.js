import Vue from 'vue';
import Vuex from 'vuex';
import { vuexSessionStorage, vuexLocalStorage } from './persist';
import modules from './modules';
import local_modules from './local_modules';

Vue.use(Vuex);

const ENABLE_STRICT = process.env.NODE_ENV !== 'production';

export const sessionStore = new Vuex.Store({
  modules,
  strict: ENABLE_STRICT,
  plugins: [vuexSessionStorage.plugin],
});

export const localStore = new Vuex.Store({
  modules: local_modules,
  strict: ENABLE_STRICT,
  plugins: [vuexLocalStorage.plugin],
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
