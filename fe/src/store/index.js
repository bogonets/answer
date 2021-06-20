import Vue from "vue";
import Vuex from "vuex";
import { vuexSessionStorage, vuexLocalStorage } from "./persist";
import modules from "./modules";
import local_modules from "./local_modules";

Vue.use(Vuex);

export const sessionStore = new Vuex.Store({
  modules,
  strict: process.env.NODE_ENV !== "production",
  plugins: [vuexSessionStorage.plugin],
});

export const localStore = new Vuex.Store({
  modules: local_modules,
  strict: process.env.NODE_ENV !== "production",
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

export const configDetailsStore = new Vuex.Store({
  state: {
    configDetails: {},
  },
  getters: {
    getConfigDetails: function(state) {
      return state.configDetails;
    },
  },
  mutations: {
    setConfigDetails(state, items) {
      state.configDetails = items;
    },
  },
});
